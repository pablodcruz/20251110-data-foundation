# 🟡 **AI-Enabled Development**

### **Prompt Engineering for Code**

**Definition:**
- **Prompt Engineering** involves crafting precise and effective instructions to guide AI language models in generating accurate and functional code tailored to specific requirements.

**Best Practices (IMPORTANT):**
- **Clarity and Specificity:** Provide clear, detailed instructions specifying the programming language, framework, and desired functionality.
  - *Example:* "Write a Python function using the Django framework that handles user authentication."
  
- **Include Examples:** Supply input-output examples or sample code snippets to illustrate expected outcomes.
  
- **Define Constraints:** Specify any limitations, such as performance requirements, security considerations, or coding standards.
  
- **Context Provision:** Provide context about the project, existing codebase, or specific challenges to ensure relevant code generation.
  
- **Iterative Refinement:** Continuously refine prompts based on the AI's outputs to achieve desired results.

**Benefits:**
- **Enhanced Productivity:** Automate routine coding tasks, allowing developers to focus on more complex aspects.
- **Improved Code Quality:** Generate code that adheres to best practices and standards.
- **Faster Prototyping:** Quickly create prototypes or proof-of-concept implementations to validate ideas.

### **5.2 AI Tools in Development**

**Use Cases:**
- **Code Generation:** Automate the creation of boilerplate code, functions, or entire modules.
  
- **Unit Testing Automation:** Generate unit tests based on code to ensure functionality and reliability.
  
- **Code Optimization:** Suggest improvements to enhance performance, readability, and maintainability.
  
- **Documentation Generation:** Automatically create comments, docstrings, and technical documentation for codebases.
  
- **Code Review Assistance:** Detect code duplication, potential vulnerabilities, and adherence to coding standards.

**Benefits:**
- **Increased Test Coverage:** Automatically generate comprehensive tests to cover various code paths.
- **Faster Development Cycles:** Reduce the time spent on repetitive tasks, accelerating overall development.
- **Consistency:** Ensure uniform coding standards and documentation across the codebase.
- **Error Reduction:** Identify and rectify potential issues early in the development process.

### **5.3 Best Practices and Ethical Considerations (IMPORTANT)**

**Best Practices:**
- **Review and Validate Outputs:** Always manually review AI-generated code to ensure accuracy, security, and compliance with project requirements.
  
- **Provide Specific Prompts:** Enhance the relevance and precision of generated code by giving detailed and context-rich instructions.
  
- **Integrate with Existing Workflows:** Seamlessly incorporate AI tools into established development and CI/CD pipelines for maximum efficiency.
  
- **Maintain Security:** Avoid using AI tools to handle sensitive data or generate security-critical code without proper oversight.
  
- **Continuous Learning:** Stay updated with advancements in AI tools and incorporate new features to improve development practices.

**Ethical Considerations:**
- **Bias and Fairness:** Ensure that AI tools do not introduce or perpetuate biases in code generation.
  
- **Accountability:** Maintain human oversight and responsibility for all AI-generated code to prevent misuse or unintended consequences.
  
- **Transparency:** Understand and communicate the capabilities and limitations of AI tools to stakeholders.
  
- **Data Privacy:** Protect sensitive information and comply with data protection regulations when using AI tools.

---

### **6.1 Difference Between Discriminative and Generative Language Models**

- **Discriminative Models**: Learn the boundary between classes (e.g., "Is this sentence positive or negative?"). They predict labels given data.  
  - *Example:* Logistic Regression, BERT (when fine-tuned for classification).
  
- **Generative Models**: Learn how data is generated. They can produce new data instances by modeling the full distribution.  
  - *Example:* GPT, which generates full text responses.

---

### **6.2 Using Prompt Engineering for Creative Writing**

- When using GenAI to generate creative writing samples:
  - **Be descriptive in tone and genre**: "Write a 300-word horror story set in a haunted library."
  - **Provide structure or character seeds**: Include prompts like "Include a plot twist and dialogue between a child and a ghost."
  - **Iterate with refinement**: Adjust tone, pacing, and creativity based on outputs.
  - **Balance originality with constraints**: Guide the AI with rules while allowing narrative freedom.

---

### **6.3 How to Prevent Hallucinations**

- **Hallucinations** refer to confident but incorrect outputs from AI.
- Prevention strategies:
  - **Add factual constraints** in the prompt
  - **Provide grounding data** (like reference text or examples)
  - **Manually review** AI output
  - **Use retrieval-augmented generation (RAG)** for fact-based completions

---

### **6.4 GitHub Copilot and How It Works**

- GitHub Copilot is an AI coding assistant powered by OpenAI Codex.
- **It provides code suggestions** directly in your IDE based on the current file and context.
- Copilot uses:
  - Context from comments and function names
  - Pattern recognition from billions of lines of code
  - Auto-completion suggestions as you type

---

### **6.5 What is AI Tooling?**

- **AI Tooling** refers to a growing suite of **AI-powered developer tools** that assist with various aspects of software development. These tools help automate repetitive tasks, improve code quality, and accelerate workflows.

#### 🔧 Tool Categories and Examples (should know 3-4 examples):

- **Code Generation Tools**  
  Help you write functions, classes, or entire files based on context or comments.
  - Examples: **GitHub Copilot**, **Tabnine**, **Amazon CodeWhisperer**, **Codeium**

- **Test Case Generators**  
  Automatically create unit tests based on function definitions and expected behavior.
  - Examples: **Diffblue Cover (for Java)**, **CodiumAI**, **Ponicode**, **Testim**

- **Documentation Tools**  
  Generate comments, docstrings, or entire technical documentation based on code.
  - Examples: **Kite**, **Mintlify**, **CodeRabbit**, **Documatic**

- **Code Review and Analysis Assistants**  
  Analyze your code for style issues, security risks, and performance improvements.
  - Examples: **DeepCode (by Snyk)**, **SonarQube AI features**, **Codiga**, **CodeGuru (AWS)**

### **6.6 Using GenAI in Code Analysis**

- GenAI can assist in code analysis by:
  - Detecting duplicated or redundant code
  - Identifying anti-patterns or bad practices
  - Recommending refactors
  - Providing inline explanations or documentation
  - Assisting with bug detection and fix suggestions

---

## **7. AI vs ML vs GenAI**

### **AI (Artificial Intelligence)**  
- Broad field focused on making machines smart  
- Includes rules, logic, learning, and decision-making  
- *Example:* Voice assistants, chatbots

### **ML (Machine Learning)**  
- Subset of AI that **learns from data**  
- Makes predictions or finds patterns  
- *Example:* Fraud detection, recommendation engines

### **GenAI (Generative AI)**  
- Subset of ML that **creates new content**  
- Generates text, code, images, etc.  
- *Example:* ChatGPT, GitHub Copilot, DALL·E

So: **AI** is the big field → **ML** is learning from data → **GenAI** is creating content from that learning.