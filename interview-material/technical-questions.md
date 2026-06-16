# Technical Q&A — Forward Deployed MLE Interview Prep

---

## 1. "Walk me through the bias-variance tradeoff."

### Answer Blueprint
- Bias = error from oversimplified assumptions → underfitting → model too simple to capture the pattern
- Variance = error from oversensitivity to training data → overfitting → model memorizes training data, fails to generalize
- Reducing one tends to increase the other
- Mitigations: regularization, cross-validation, ensemble methods, more training data

### Cleaned Transcript
> "The bias-variance tradeoff describes a fundamental tension in model training. Bias is error from oversimplified assumptions — a high-bias model underfits, meaning it can't capture the real pattern in the data. Variance is error from oversensitivity to the training data — a high-variance model overfits, meaning it memorizes the training data but fails to generalize. The tradeoff is that reducing one tends to increase the other. In practice you manage it a few ways: regularization to penalize complexity and reduce variance, cross-validation to detect overfitting early, ensemble methods like random forests that average out high-variance models, and simply getting more training data, which reduces variance without increasing bias."

---

## 2. "Explain precision, recall, and F1. When would you optimize for each?"

### Answer Blueprint
- Precision = TP / (TP + FP) — of everything predicted positive, how many actually were
- Recall = TP / (TP + FN) — of everything actually positive, how many did we catch
- F1 = harmonic mean of both — use when classes are imbalanced and both matter equally
- Why not accuracy: misleading with imbalanced classes — predicting everyone healthy still gives high accuracy
- Optimize recall when false negatives are costly: disease screening, fraud, the ACLU auditor
- Optimize precision when false positives are costly: spam filtering, stock prediction, legal evidence

### Cleaned Transcript
> "Precision, recall, and F1 are all classification metrics. Precision is true positive over true positive plus false positive — of everything the model predicted positive, what proportion actually was. Recall is true positive over true positive plus false negative — of everything that actually was positive, what proportion did we catch. F1 is the harmonic mean of both. The reason we need these beyond accuracy is that accuracy is misleading with imbalanced classes — if almost nobody has a disease, predicting everyone as healthy still gives high accuracy. For the ACLU auditor, we optimized for recall because we were running multiple classifiers across thousands of videos. We didn't care about false positives — if a video got flagged incorrectly, an attorney could dismiss it. What we couldn't afford was a false negative, because a real violation would get buried. For something like stock prediction, you'd flip that and optimize for precision — it's worse to be wrong than to miss an opportunity. F1 is the right choice when both matter equally and you're dealing with imbalanced classes."

---

## 3. "What's the difference between zero-shot, few-shot, and fine-tuning? When would you use each?"

### Answer Blueprint
- All three are ways to use pretrained models, in increasing order of effort and data required
- Zero-shot: use model as-is, no examples — best for general tasks the model already handles well
- Few-shot: give examples in the prompt to steer output format or domain-specific behavior
- Fine-tuning: update model weights with labeled data — use when task is specialized and general models underperform
- Decision rule: zero-shot first → few-shot if output needs steering → fine-tune only with labeled data and a specialized task

### Cleaned Transcript
> "Zero-shot, few-shot, and fine-tuning are three ways to use pretrained models, in increasing order of effort and data required. Zero-shot is using a model as-is — no examples, no retraining. This works well for general tasks the model was trained on. At the ACLU, we used zero-shot BERT classifiers to detect whether a transcription contained the full start and end of an officer interaction — a general enough concept that a pretrained model handles it well. Few-shot is where you include examples in the prompt to steer the model's output. I use this when I want a very specific output format — like asking an LLM to generate Anki flashcards as a CSV and including an example of the exact format I want. It's not exclusive to LLMs, but it's especially useful there. Fine-tuning is where you actually update model weights using labeled data to specialize the model for a specific task. For the ACLU auditor, if we wanted to classify whether a stated stop reason was legally justified, we'd need an attorney to manually label examples — there's no way a general model is a legal expert. The decision rule is: start zero-shot, move to few-shot if you need to control output behavior, and only fine-tune when you have labeled data and the task is specialized enough that general models consistently underperform."

---

## 4. "How do transformers work? Explain it at a conceptual level."

### Answer Blueprint
- Problem they solve: RNNs processed tokens sequentially — slow, poor long-range dependencies
- Core idea: attention — look at the entire input at once, compute for each token how much it should attend to every other token
- Query = what this token is looking for; Key = what this token contains; Value = what this token contributes
- Query × Key → attention weights; weights × Values → context-aware representation of each token
- Multi-head attention: run this multiple times in parallel, each head learns different relationship types
- Three archetypes: Encoder (BERT) — full sequence, good for classification; Decoder (GPT) — generates one token at a time, causal masking; Encoder-Decoder (T5) — reads input, generates output, good for translation/summarization

### Cleaned Transcript
> "Transformers solve the biggest problem with RNNs — sequential processing. RNNs had to take in tokens one at a time, which made training slow and made long-range dependencies hard to capture. Transformers fix this by processing the entire sequence at once using attention. The mechanism works by splitting each token into three vectors: a query, a key, and a value. The query represents what information that token is looking for. Take the sentence 'the animal went to the farm and it ran' — the word 'it' is looking for its referent, which is 'animal.' The key represents what that token contains semantically — 'king' and 'queen' are close in key space, both very different from 'animal.' The value is what actually gets retrieved. Query and key are compared to produce attention weights — how much should each token attend to every other token. Those weights are then applied to the values to produce a context-aware representation of each token. The key insight is that this happens for all tokens simultaneously, which makes training dramatically faster. Multi-head attention runs this process multiple times in parallel, where each head learns to attend to different types of relationships. There are three transformer archetypes: encoders like BERT take in the full sequence at once and are great for classification. Decoders like GPT generate one token at a time, where each token can only attend to previous tokens. And encoder-decoders like the original transformer use an encoder to read the input into abstract features and a decoder to generate an output — great for translation and summarization."

---

## 5. "What is RAG and when would you use it over fine-tuning?"

### Answer Blueprint
- RAG solves the problem of LLMs having frozen knowledge and no access to private data
- Three steps: Retrieve relevant chunks from a knowledge base using embedding similarity → Augment the prompt with those chunks → Generate using both pretrained knowledge and retrieved context
- RAG when the problem is what the model knows (dynamic or private data)
- Fine-tune when the problem is how the model behaves (tone, format, domain style)
- Not mutually exclusive — production systems often combine both
- Personal example: franchise quiz retrieves Fandom wiki pages and injects them into the prompt

### Cleaned Transcript
> "RAG stands for retrieval augmented generation. It solves the problem of LLMs having knowledge frozen at training time and no access to private or dynamic data. The way it works is: take the user's input, retrieve semantically relevant chunks from a knowledge base using embedding similarity, inject those chunks into the prompt as context, and then generate a response using both the model's pretrained knowledge and the retrieved information. I actually built a version of this in my franchise quiz — when a user inputs a franchise, the system retrieves relevant pages from Fandom wikis and injects them into the prompt so the model can generate grounded, lore-accurate responses. Where you'd use fine-tuning instead is when the problem is about how the model behaves rather than what it knows — output format, tone, domain-specific style. The clean decision rule is: RAG when the problem is what the model knows, fine-tune when the problem is how the model behaves. They're not mutually exclusive — production systems often combine both, fine-tuning for consistent behavior and RAG for current information."

---

## 6. "What are embeddings and how does vector similarity search work?"

### Answer Blueprint
- Embedding = a high-dimensional vector representation of something (word, sentence, image, quiz response)
- Vector similarity = measuring how alike two vectors are; cosine similarity measures the angle between vectors, not their distance — two vectors pointing the same direction are similar regardless of magnitude
- Perpendicular vectors = dissimilar; parallel vectors = similar
- Personal example: franchise quiz uses cosine similarity to match user quiz responses to character response vectors
- Most common use case: RAG — embed user query, find most similar document chunks, retrieve and inject

### Cleaned Transcript
> "An embedding is a high-dimensional vector used to represent something — a word, a sentence, an image, or in my case, a set of quiz responses. The idea is that semantically similar things end up close together in that vector space. Vector similarity search works by comparing how alike two vectors are. Cosine similarity specifically measures the angle between two vectors rather than their distance — so two vectors pointing in the same direction are considered similar even if one is much longer than the other. Perpendicular vectors represent completely dissimilar things. I built this directly into my franchise personality quiz. The system has an LLM roleplay as each character and answer all 15 quiz questions. Those responses become character embedding vectors. When a user completes the quiz, their responses are embedded the same way and compared via cosine similarity to every character. The character — and therefore the class, like a Hogwarts house — with the highest average similarity to the user's responses is the result. The most common production use case for this is RAG — you embed the user's query, search a vector database for the most semantically similar document chunks, and retrieve those to inject into the prompt."
