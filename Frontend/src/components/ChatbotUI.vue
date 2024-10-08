<template>
  <div>
    <!-- Chatbot Toggle Button when chatbot is closed -->
    <button v-if="!isChatbotOpen" class="chatbot-toggle-btn" @click="toggleChatbot">
      <i class="fas fa-comments"></i>
    </button>

    <!-- Chatbot Panel -->
    <transition name="slide">
      <div v-if="isChatbotOpen" :class="['chatbot-container', { 'expanded': isExpanded }]">
        <div class="chatbot-header">
          <img src="@/assets/image1.png" alt="Institution Logo" class="logo" />
          <h3 class="chatbot-title">Institute Support</h3>
          <button class="expand-chatbot-btn" @click="toggleExpand">
            <i :class="isExpanded ? 'fas fa-compress' : 'fas fa-expand'"></i>
          </button>
          <button class="close-chatbot-btn" @click="toggleChatbot">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="chatbot-window" ref="chatWindow">
          <div v-for="(message, index) in messages" :key="index" :class="messageClass(message.type)">
            <div class="message" v-html="message.text"></div>
          </div>
        </div>

        <div class="chatbot-input-area">
          <input
            type="text"
            v-model="userInput"
            @keydown.enter="sendMessage"
            placeholder="Type your question here..."
            class="input-field"
          />
          <button @click="sendMessage" class="send-btn">
            <i class="fas fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      isChatbotOpen: false,
      isExpanded: false,
      userInput: "",
      messages: [
        {
          text: "Welcome to VIT Pune! How may I assist you today?",
          type: "bot",
        },
      ],
    };
  },
  methods: {
    toggleChatbot() {
      this.isChatbotOpen = !this.isChatbotOpen;
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
    async sendMessage() {
      if (this.userInput.trim() !== "") {
        this.messages.push({ text: this.userInput, type: "user" });
        const inputText = this.userInput;
        this.userInput = "";

        this.$nextTick(() => {
          const chatWindow = this.$refs.chatWindow;
          chatWindow.scrollTop = chatWindow.scrollHeight;
        });

        try {
          const response = await axios.post("http://localhost:5000/api/query", {
            query: inputText,
          });

          const botResponse = response.data.response;
          const formattedResponse = this.formatBotResponse(botResponse);

          this.messages.push({ text: formattedResponse, type: "bot" });

          this.$nextTick(() => {
            const chatWindow = this.$refs.chatWindow;
            chatWindow.scrollTop = chatWindow.scrollHeight;
          });
        } catch (error) {
          console.error("Error fetching bot response:", error);
          this.messages.push({
            text: "There was an error processing your request.",
            type: "bot",
          });
        }
      }
    },
    messageClass(type) {
      return type === "user" ? "user-message" : "bot-message";
    },
    formatBotResponse(botResponse) {
      const pattern = /"answer":\s*"(.*?)"/s;
      const match = pattern.exec(botResponse);
      if (match) {
        let formattedText = match[1];
        formattedText = formattedText.replace(/\\n/g, "\n").replace(/\\"/g, '"');
        formattedText = formattedText.replace(/^Details:\s*/, "");

        formattedText = formattedText
          .replace(/\b(?:https?|ftp):\/\/[^\s/$.?#].[^\s]*\b/g, (url) => {
            return `<a href="${url}" target="_blank" class="hyperlink">${url}</a>`;
          })
          .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, (email) => {
            return `<span class="highlight">${email}</span>`;
          })
          .replace(/\b\d{2,3}\s?[-]?\s?\d{4}\s?[-]?\s?\d{4,5}\b/g, (phone) => {
            return `<span class="highlight">${phone}</span>`;
          });
        return formattedText;
      }
    },
  },
};
</script>

<style scoped>
/* Main container */
.chatbot-container {
  width: 350px;
  height: 500px;
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  font-family: "Roboto", sans-serif;
  z-index: 1000;
  transition: all 0.3s ease-in-out;
}

/* Expanded Chatbot Container */
.expanded {
  width: 700px;
  height: 600px;
}

/* Chatbot Toggle Button */
.chatbot-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #004f9e;
  color: white;
  border: none;
  padding: 18px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 1100;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.chatbot-toggle-btn:hover {
  background-color: #003d7b;
  transform: scale(1.1);
}

.chatbot-toggle-btn i {
  font-size: 22px;
}

/* Header */
.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #f7f9fc;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  border-bottom: 1px solid #e6e6e6;
}

.logo {
  width: 40px;
  margin-right: 10px;
}

.chatbot-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.expand-chatbot-btn,
.close-chatbot-btn {
  background-color: transparent;
  border: none;
  color: #555;
  font-size: 18px;
  cursor: pointer;
}

.expand-chatbot-btn i,
.close-chatbot-btn i {
  font-size: 18px;
}

/* Chat Window */
.chatbot-window {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  background-color: #f4f7f9;
}

.expanded .chatbot-window {
  height: 550px;
}

.message {
  padding: 10px 12px;
  border-radius: 16px;
  max-width: 100%;
  word-wrap: break-word;
  font-size: 14px;
}

.bot-message {
  background-color: #e6e6e6;
  color: #333;
  align-self: flex-start;
  text-align: left;
}

.user-message {
  background-color: #004f9e;
  color: #ffffff;
  margin-top: 10px;
  margin-bottom: 10px;
  align-self: flex-start;
  text-align: right;
}

/* Input Area */
.chatbot-input-area {
  display: flex;
  padding: 12px 15px;
  background-color: #ffffff;
  border-top: 1px solid #e6e6e6;
}

.input-field {
  flex: 1;
  padding: 10px 12px;
  font-size: 14px;
  border: 1px solid #cccccc;
  border-radius: 25px;
  outline: none;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #004f9e;
}

.send-btn {
  background-color: #004f9e;
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 25px;
  margin-left: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.send-btn i {
  font-size: 16px;
}

.send-btn:hover {
  background-color: #003d7b;
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-enter,
.slide-leave-to {
  transform: translateY(100%);
}

/* Hyperlink styling */
.hyperlink {
  color: #004f9e;
  text-decoration: underline;
  cursor: pointer;
}

/* Highlight class for emails and phone numbers */
.highlight {
  background-color: #ffe200;
  padding: 1px 4px;
  border-radius: 3px;
}
</style>
