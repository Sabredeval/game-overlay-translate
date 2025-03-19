# Overlay Trans

Overlay Trans is a desktop application designed to help users learn new languages and enhance their vocabulary. The app provides a variety of tools and features to make language learning interactive, engaging, and efficient. Whether you're a beginner or an advanced learner, Overlay Trans aims to be your go-to companion for mastering a new language.

---

### **Project Structure**

Project follows MVC pattern. Every instance of UI (page, tab) is divided to view and controller for better maintainability. 

- core - Main application components
- common - Shared utilities and styling
- data - Data persistence layer
- pages - Secondary windows
- tabs - Main page notebook pads
- util - Utility functions
- resources - Static assets
- app.py - Entry point of the program

## Overlay Trans - Software Features 
<i> Planned and current

### Core Features

#### UI/UX
- [✓] Basic interface
- [✓] Enhanced UI/UX
- [✓] Settings panel
  - [✓] Dark mode
  - [✓] Font size adjustments
  - [✓] Keyboard shortcuts

#### Text Selection Tool
- [✓] Basic functionality
- [ ] Ensure correct functionality in all contexts
- [ ] Connect to reading assistant

#### Dictionary Integration
- [ ] Improve `Wiktionary` parsing with `BeautifulSoup`
- [ ] Optimize performance with categorization and lazy loading
- [ ] Add favorites system for `Wiktionary` pages

### Database

#### Word Storage
- [✓] Basic save words functionality
- [ ] Expand storage capabilities
- [ ] Add categorization for saved words
- [ ] Allow saving favorite `Tatoeba` sentences

### Language Processing

#### Analysis Tools
- [ ] Parts of speech analysis
- [ ] Lemma finder (basic word form detection)
- [ ] spaCy integration for tokenization, stemming, and POS tagging

#### Language Support
- [✓] English
- [ ] Spanish
- [ ] German
- More in future...

### Learning Features

#### Reading Assistant
- [ ] Import `PDF`/`FB2`/`EPUB` documents
- [ ] Import text via shortcut
- [ ] Connect selection tool
- [ ] Integrate language analyzer tool
- [✓] Add unknown words to vocabulary with one click

#### Vocabulary Builder
- [ ] Create visually appealing word lists
- [ ] Add/edit/delete word collections
- [ ] Organize by categories/difficulty/frequency

#### Interactive Learning (Gamification)
- [ ] `Flash cards` for vocabulary practice
- [ ] `Fill-in-the-blank` exercises for contextual learning
- [ ] `Sentence builder` for word ordering practice
- [ ] `Parts of speech identifier` for grammar understanding
- [ ] `Word matching` for vocabulary practice

#### Study Dashboard
- [ ] Visual statistics and progress tracking
- [ ] Learning streak and achievement system
- [ ] Performance analytics

### Non-Priority Improvements
- [ ] Word translation pop-up
- [ ] Full text translation functionality
</i>
---

### **Dependencies**
- Python 3.8 or higher
- Required libraries: `tkinter`, `requests`, `beautifulsoup4`, `pynput`, `pystray`, `Pillow`, `pyserract`