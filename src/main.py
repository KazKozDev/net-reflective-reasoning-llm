import asyncio
import aiohttp
import json
import re
from typing import List, Dict, Optional, Union, Tuple
from datetime import datetime, timedelta
from enum import Enum
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import hashlib
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse

class ThoughtProcess(Enum):
	INITIAL_THOUGHTS = "initial_thoughts"
	SEARCH_REQUIRED = "search_required"
	ANALYSIS = "analysis"
	CRITIQUE = "critique"
	REFINEMENT = "refinement"
	FINAL_ANSWER = "final_answer"
	
class ReasoningChain:
	def __init__(self):
		self.thoughts: List[Dict] = []
		
	def add_thought(self, process: ThoughtProcess, content: str, confidence: float):
		self.thoughts.append({
			"process": process,
			"content": content,
			"confidence": confidence,
			"timestamp": datetime.now()
		})
		
	def get_reasoning_history(self) -> str:
		return "\n\n".join([
			f"{thought['process'].value}:\n{thought['content']}\nConfidence: {thought['confidence']:.2f}"
			for thought in self.thoughts
		])
	
class Message:
	def __init__(self, role: str, content: str, reasoning: Optional[ReasoningChain] = None):
		self.role = role
		self.content = content
		self.timestamp = datetime.now()
		self.reasoning = reasoning or ReasoningChain()
		
class Conversation:
	def __init__(self, max_context_length: int = 4096):
		self.messages: List[Message] = []
		self.max_context_length = max_context_length
		
	def add_message(self, role: str, content: str, reasoning: Optional[ReasoningChain] = None):
		self.messages.append(Message(role, content, reasoning))
		self._trim_context()
		
	def get_context(self, include_reasoning: bool = True) -> str:
		result = []
		for msg in self.messages:
			message_text = f"{msg.role}: {msg.content}"
			if include_reasoning and msg.reasoning and msg.reasoning.thoughts:
				message_text += f"\nReasoning:\n{msg.reasoning.get_reasoning_history()}"
			result.append(message_text)
		return "\n\n".join(result)
	
	def _trim_context(self):
		while len(self.get_context()) > self.max_context_length:
			self.messages.pop(0)
			
class WebSearchManager:
	def __init__(self):
		self.search_cache = {}
		self.parsing_cache = {}
		self.iteration_results_cache = {}
		self.max_iterations = 1
		
	def get_current_datetime(self):
		return datetime.now().strftime("%d %B %Y, %H:%M:%S")
	
	async def analyze_intent(self, llm, input_text: str) -> str:
		intent_prompt = f"""
		Analyze the following user text and determine the main intent. Follow these steps:

		1. Identify key words and phrases indicating user's goal
		2. Determine if user is seeking information, trying to perform an action, or asking for help
		3. Consider context: time (now, past, future), location, specific details
		4. Consider possible hidden intents or subtext
		5. Consider alternative interpretations
		6. Determine the main goal combining all previous steps

		Respond with ONE brief sentence accurately describing the user's main intent.

		User text: {input_text}

		Intent:
		"""
		
		return await llm._generate(intent_prompt, temp_override=0.3)
	
	async def generate_search_query(self, llm, input_text: str, user_intent: str, iteration: int = 1) -> str:
		current_date = datetime.now()
		yesterday = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
		
		query_prompt = f"""
		Current date: {current_date.strftime("%Y-%m-%d")}
		Yesterday: {yesterday}

		Create an effective search query based on:
		Text: {input_text}
		Intent: {user_intent}
		Iteration: {iteration} of {self.max_iterations}

		Rules for query generation:
		1. Use appropriate search operators if needed:
			- "exact phrase"
			- -exclude
			- site:domain.com
			- filetype:pdf
		2. Use 0-7 key words/phrases from user's text
		3. Focus on missing information from previous iteration if iteration > 1 

		Return only the new search query, no explanation:
		"""
		
		query = await llm._generate(query_prompt, temp_override=0.3)
		return self._post_process_query(query)
	
	def _post_process_query(self, query: str) -> str:
		query = query.strip('"').strip("'")
		query = re.sub(r'^(query:|search:)\s*', '', query, flags=re.IGNORECASE)
		query = re.sub(r'\s+', ' ', query)
		return query.strip()
	
	def get_search_results(self, query: str) -> List[Dict]:
		if query in self.search_cache:
			print(f"Using cached search results for query: {query}")
			return self.search_cache[query]
		
		search = DDGS()
		try:
			results = list(search.text(query, max_results=9))
			self.search_cache[query] = results
			return results
		except Exception as e:
			print(f"Search error: {e}")
			return []
		
	def choose_urls_to_parse(self, results: List[Dict], max_urls: int = 3) -> List[str]:
		return [result['href'] for result in results[:max_urls]]
	
	def parse_webpage(self, url: str) -> Optional[Dict]:
		cache_key = hashlib.md5(url.encode()).hexdigest()
		if cache_key in self.parsing_cache:
			return self.parsing_cache[cache_key]
		
		try:
			if self._is_static_site(url):
				content = self._parse_static_site(url)
			else:
				content = self._parse_dynamic_site(url)
				
			if content:
				parsed = self._parse_generic(content)
				
				if parsed:
					self.parsing_cache[cache_key] = parsed
					return parsed
				
		except Exception as e:
			print(f"Error parsing {url}: {e}")
			return None
		
	def _is_static_site(self, url: str) -> bool:
		try:
			response = requests.get(url, timeout=5)
			return response.status_code == 200 and '<html>' in response.text.lower()
		except:
			return False
		
	def _parse_static_site(self, url: str) -> Optional[str]:
		try:
			process = CrawlerProcess({
				'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
			})
			spider = StaticSpider(start_urls=[url])
			process.crawl(spider)
			process.start()
			return spider.content
		except Exception as e:
			print(f"Static parsing error: {e}")
			return None
		
	def _parse_dynamic_site(self, url: str) -> Optional[str]:
		try:
			response = requests.get(url, timeout=10)
			return response.text
		except Exception as e:
			print(f"Dynamic parsing error: {e}")
			return None
		
	def _parse_generic(self, content: str) -> Optional[Dict]:
		soup = BeautifulSoup(content, 'html.parser')
		return {
			'title': soup.find('h1').text.strip() if soup.find('h1') else "",
			'content': '\n'.join([p.text.strip() for p in soup.find_all('p') if p.text.strip()])
		}
	
class StaticSpider(scrapy.Spider):
	name = 'static_spider'
	content = ""
	
	def parse(self, response):
		paragraphs = response.css('p::text').getall()
		self.content = "\n".join(paragraphs)
		
class EnhancedLLM:
	def __init__(
		self,
		name: str,
		base_url: str = "http://localhost:11434/api",
		context_length: int = 4096,
		temperature: float = 0.4,
		top_p: float = 0.9
	):
		self.name = name
		self.base_url = base_url
		self.context_length = context_length
		self.temperature = temperature
		self.top_p = top_p
		self.conversation = Conversation(max_context_length=context_length)
		self.web_search = WebSearchManager()
		
	async def _generate(self, prompt: str, temp_override: Optional[float] = None) -> str:
		async with aiohttp.ClientSession() as session:
			try:
				async with session.post(
					f"{self.base_url}/generate",
					json={
						"model": self.name,
						"prompt": prompt,
						"temperature": temp_override or self.temperature,
						"top_p": self.top_p,
						"stream": True
					},
					headers={'Accept': 'application/x-ndjson'},
					timeout=aiohttp.ClientTimeout(total=180)
				) as response:
					response.raise_for_status()
					result = ""
					async for line in response.content:
						try:
							data = json.loads(line)
							if 'response' in data:
								chunk = data['response']
								result += chunk
								print(chunk, end='', flush=True)
						except json.JSONDecodeError:
							continue
					print()
					return result.strip()
			except Exception as e:
				error_msg = f"Error generating response: {str(e)}"
				print(error_msg)
				return error_msg
			
	async def evaluate_knowledge(self, query: str) -> Tuple[bool, float, str]:
		evaluation_prompt = f"""
		Evaluate if you have sufficient knowledge to answer this query: "{query}"
		
		Follow these steps:
		1. Identify key facts, dates, or data needed to answer
		2. For each piece of information needed:
			- Do you have reliable knowledge about it?
			- Is it likely to change frequently?
			- Does it require verification from current sources?
		3. Consider temporal aspects:
			- Is this about historical facts you know well?
			- Does it require current/real-time information?
			- Has this information likely changed recently?
		
		Respond in this exact format:
		NEEDS_SEARCH: [Yes/No]
		CONFIDENCE: [0-1]
		REASON: [Brief explanation]
		"""
		
		result = await self._generate(evaluation_prompt, temp_override=0.3)
		
		lines = result.strip().split('\n')
		needs_search = 'yes' in lines[0].lower()
		confidence = float(lines[1].split(':')[1].strip())
		reason = lines[2].split(':')[1].strip()
		
		return needs_search, confidence, reason
	
	async def process_query(self, query: str) -> Tuple[str, ReasoningChain]:
		reasoning = ReasoningChain()
		
		print("\n🤔 Evaluating knowledge base...", end=' ', flush=True)
		needs_search, confidence, reason = await self.evaluate_knowledge(query)
		
		reasoning.add_thought(
			ThoughtProcess.INITIAL_THOUGHTS,
			f"Initial evaluation: {reason}\nConfidence level: {confidence:.2f}\nNeed external search: {needs_search}",
			confidence
		)
		
		if not needs_search and confidence > 0.7:
			print("\n🧠 Analyzing with existing knowledge...", end=' ', flush=True)
			analysis = await self._generate(
				f"Question: {query}\n\n"
				f"Let's analyze this step by step:\n"
				f"1. What specific facts do we know about this?\n"
				f"2. What are the key aspects to consider?\n"
				f"3. How reliable is our existing knowledge?\n"
				f"Provide concrete facts and explain reasoning.",
				temp_override=0.3
			)
			reasoning.add_thought(ThoughtProcess.ANALYSIS, analysis, confidence)
			
			print("\n⚖️ Critical evaluation...", end=' ', flush=True)
			critique = await self._generate(
				f"Given this analysis:\n{analysis}\n\n"
				f"Let's critically evaluate:\n"
				f"1. Which parts are we most certain about?\n"
				f"2. What might need verification?\n"
				f"3. Are there any potential biases or gaps?\n"
				f"Be specific about confidence levels.",
				temp_override=0.3
			)
			reasoning.add_thought(ThoughtProcess.CRITIQUE, critique, 0.85)
			
		else:
			print("\n🔍 Initiating web search...", end=' ', flush=True)
			user_intent = await self.web_search.analyze_intent(self, query)
			
			search_query = await self.web_search.generate_search_query(
				self, query, user_intent, 1
			)
			print(f"\nSearch query: {search_query}")
			
			search_results = self.web_search.get_search_results(search_query)
			if search_results:
				print(f"\nFound {len(search_results)} results")
				urls_to_parse = self.web_search.choose_urls_to_parse(search_results)
				
				parsed_contents = {}
				for url in urls_to_parse:
					content = self.web_search.parse_webpage(url)
					if content:
						parsed_contents[url] = content
						print(f"\nParsed content from: {url}")
						
				if parsed_contents:
					analysis = await self._generate(
						f"Analyze these search results for: {query}\n\n" +
						"\n".join([
							f"Source {i+1} ({url}):\nTitle: {content['title']}\n{content['content'][:1000]}"
							for i, (url, content) in enumerate(parsed_contents.items())
						]) +
						"\n\nProvide a detailed analysis:\n"
						"1. Key facts and figures found\n"
						"2. Credibility of sources\n"
						"3. Consistency across sources\n"
						"4. Any conflicting information",
						temp_override=0.4
					)
					reasoning.add_thought(ThoughtProcess.ANALYSIS, analysis, 0.8)
					
					print("\n⚖️ Evaluating findings...", end=' ', flush=True)
					critique = await self._generate(
						f"Review the search results and analysis:\n{analysis}\n\n"
						"Critically evaluate:\n"
						"1. Reliability of information\n"
						"2. Potential biases or limitations\n"
						"3. Areas needing more verification\n"
						"4. Confidence in different aspects",
						temp_override=0.3
					)
					reasoning.add_thought(ThoughtProcess.CRITIQUE, critique, 0.85)
					
		# Generate final answer with current timestamp
		print("\n📝 Synthesizing final answer...", end=' ', flush=True)
		current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
		
		final_prompt = (
			f"Current timestamp: {current_time}\n\n"
			f"Based on our complete analysis:\n\n"
			f"Question: {query}\n\n"
			f"Reasoning chain:\n{reasoning.get_reasoning_history()}\n\n"
			f"Provide a comprehensive answer that:\n"
			f"1. Directly addresses the question\n"
			f"2. Incorporates the most reliable information\n"
			f"3. Acknowledges any uncertainties\n"
			f"4. Uses the provided timestamp when discussing current events or timely information\n"
			f"5. Cites sources where relevant\n"
			f"Make the response clear, concise, and well-structured."
		)
		
		final_answer = await self._generate(final_prompt, temp_override=0.4)
		reasoning.add_thought(ThoughtProcess.FINAL_ANSWER, final_answer, 0.95)
		
		return final_answer, reasoning
	
class AdvancedGPTLike:
	def __init__(
		self,
		model_name: str = "gemma2:9b",
		system_prompt: Optional[str] = None
	):
		self.model = EnhancedLLM(model_name)
		self.system_prompt = system_prompt or (
			"You are an advanced AI assistant specialized in providing accurate, concise, "
			"and factual information. When asked questions:\n"
			"1. First analyze if you can answer directly from your knowledge\n"
			"2. If needed, use web search to find current and accurate information\n"
			"3. Provide specific numbers and data when available\n"
			"4. Break down complex information into clear categories\n"
			"5. Include sources when using external information\n"
			"Keep responses focused and precise. Verify information when possible."
		)
		self.model.conversation.add_message("system", self.system_prompt)
		
	async def chat(self):
		print("\nNet Reflective Reasoning LLM v1.0.0")
		print("A web search framework using Ollama")
		print("Powered by 'Gemma2:9B'\n")
		
		last_reasoning = None
		
		while True:
			try:
				user_input = input("\nYou: ").strip()
				
				if not user_input:
					continue
				
				if user_input.lower() in ['quit', 'exit']:
					print("\nGoodbye! 👋")
					break
				
				if user_input.lower() == 'clear':
					self.model.conversation = Conversation(self.model.context_length)
					self.model.conversation.add_message("system", self.system_prompt)
					print("\n🧹 Conversation history cleared.")
					continue
				
				if user_input.lower() == 'explain' and last_reasoning:
					print("\n🔍 Reasoning Chain:")
					print("=" * 50)
					for thought in last_reasoning.thoughts:
						print(f"\n{thought['process'].value.upper()}:")
						print(f"Confidence: {thought['confidence']:.2f}")
						print("-" * 30)
						print(thought['content'])
					print("\n" + "=" * 50)
					continue
				
				if user_input.lower().startswith('system '):
					self.system_prompt = user_input[7:].strip()
					self.model.conversation = Conversation(self.model.context_length)
					self.model.conversation.add_message("system", self.system_prompt)
					print("\n⚙️ System prompt updated.")
					continue
				
				context = self.model.conversation.get_context()
				print("\nAssistant:", end=' ', flush=True)
				
				try:
					response, reasoning = await self.model.process_query(user_input)
					last_reasoning = reasoning
					
					self.model.conversation.add_message("user", user_input)
					self.model.conversation.add_message("assistant", response, reasoning)
					
					print("\n💡 Type 'explain' to see my reasoning process")
					
				except Exception as e:
					print(f"\n❌ Error processing query: {str(e)}")
					continue
				
			except KeyboardInterrupt:
				print("\n\n⚠️ Interrupted. Type 'quit' to exit or continue with your question.")
			except Exception as e:
				print(f"\n❌ An error occurred: {str(e)}")
				
async def main():
	try:
		system = AdvancedGPTLike(model_name="gemma2:9b")
		await system.chat()
	except Exception as e:
		print(f"Fatal error: {str(e)}")
		
if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\n\nProgram terminated by user.")
		
		