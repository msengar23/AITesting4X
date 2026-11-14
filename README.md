# AITesting4X

Hands-on course materials and projects for **AI-assisted software testing**. Each chapter is a self-contained folder with the prompts, apps, workflows, and notes built along the way, from prompt engineering and local LLMs to RAG, AI agents, MCP servers, and LLM evaluation.

**Author:** Mamta Singh Sengar

## Repository Structure

| Folder | Topic | What's inside |
|---|---|---|
| `chapter_01_LLM_BASICS/` | LLM basics | Anti-hallucination rules and foundational notes |
| `chapter_02_Prompt_Eng/` | Prompt engineering | Prompt design practice for test work |
| `chapter_03_Local_TC_Generator/` | Local test case generator | Streamlit app that generates test cases from Jira issues using Ollama or Groq |
| `chapter_04_JobKitAI/` | JobKitAI | Resume tailoring helper and generated resume outputs |
| `chapter_05_Local_TestCase_Generator/` | Job Tracker ATS | Local-first job application tracker (React + TypeScript + Vite) with ATS keyword insights |
| `chapter_06_Branding_LinkedinSkills/` | Branding and LinkedIn | Claude/Codex skill that turns a content seed into a publish-ready content pack |
| `chapter_07_AI_Agents/` | AI agents | Test Plan Agent that builds a Markdown test plan from a Jira issue ID |
| `chapter_08_n8n/` | n8n workflows | Bug triage, RCA, test case creation, and social post agents |
| `chapter_09_LangFlow/` | LangFlow | Bug triage agent flows and a React chat UI for them |
| `chapter_10_RAG_Basics/` | RAG basics | RAG Explorer: chunk, embed, store, and question a PDF |
| `chapter_11_RAG_Implementation/` | RAG implementation | Naive and advanced RAG flows in LangFlow and n8n |
| `chapter_12_RAG_QA_BuddyAI/` | QABuddy.ai | Multi-source hybrid RAG that answers QA questions with citations |
| `chapter_13_MCP_Basics/` | MCP basics | MCP Inspector notes |
| `chapter_14_MCP_Create_VIBE/` | MCP servers | TestCreator MCP and TestSkill Finder MCP servers |
| `chapter_15_Python_PyTest/` | Python and PyTest | Python and PyTest test automation material |
| `chapter_16_AI_Agent_Crew_AI/` | CrewAI | Coming soon (placeholder) |
| `chapter_17_AI_Agent_LangChain/` | LangChain | Coming soon (placeholder) |
| `chapter_18_AI_Agent_LangGraph/` | LangGraph | Coming soon (placeholder) |
| `chapter_19_LLM_Eval/` | LLM evaluation | Coming soon (placeholder) |
| `chapter_20_DeepEval_Basics/` | DeepEval basics | Coming soon (placeholder) |
| `chapter_21_DeepEval_Framework/` | DeepEval framework | Coming soon (placeholder) |
| `LiveClass_Tasks/` | Live class tasks | Practice tasks from live sessions, including Python exercises and QA task folders |
| `captures/` | Screenshots | Captures of deployed apps |
| `learnings/` | Notes | Dated learning notes from building the chapters |
| `ui_screenshotbugAIAgent/` | Screenshot bug reporter | UI for the screenshot-to-Jira bug reporter workflow |

Chapters with their own setup instructions have a `README.md` inside their folder. Start there before running anything.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/msengar23/AITesting4X.git
   cd AITesting4X
   ```

2. Open the chapter you want to work on and follow its `README.md`.

3. Keep credentials out of git. Copy any `.env.example` to `.env` and fill in your own keys. `.env` files are ignored by `.gitignore`.

## Prerequisites

Requirements vary by chapter. Common tools:

- **Python** for the Streamlit apps, RAG Explorer, the Test Plan Agent, and the PyTest material (each has a `requirements.txt`)
- **Node.js** for the React and Vite apps (Job Tracker ATS, Bug Triage UI, Screenshot Bug Reporter)
- **Ollama** for running local LLMs, or a **Groq** API key for hosted models
- **n8n** and **LangFlow** for the workflow chapters

## Contributing

This is a personal course repository. Issues and suggestions are welcome. For changes, open an issue first to discuss what you would like to change.

