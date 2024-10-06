<template>
  <div>
    <!-- Chatbot Toggle Button when chatbot is closed -->
    <button
      v-if="!isChatbotOpen"
      class="chatbot-toggle-btn"
      @click="toggleChatbot"
    >
      <i class="fas fa-comments"></i> <!-- Chat Icon -->
    </button>

    <!-- Chatbot Panel -->
    <transition name="slide">
      <div v-if="isChatbotOpen" :class="['chatbot-container', { 'expanded': isExpanded }]">
        <div class="chatbot-header">
          <img src="@/assets/image1.png" alt="Institution Logo" class="logo" />
          <h3 class="chatbot-title">Healthcare Support</h3> 
          <button class="expand-chatbot-btn" @click="toggleExpand">
            <i :class="isExpanded ? 'fas fa-compress' : 'fas fa-expand'"></i> <!-- Expand/Compress Icon -->
          </button>
          <button class="close-chatbot-btn" @click="toggleChatbot">
            <i class="fas fa-times"></i> <!-- Close Icon -->
          </button>
        </div>

        <div class="chatbot-window" ref="chatWindow">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="messageClass(message.type)"
          >
            <div class="message">{{ message.text }}</div>
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
      isChatbotOpen: false,  // Control whether the chatbot is open or closed
      isExpanded: false,     // Control whether the chatbot window is expanded
      userInput: "",
      messages: [
        {
          text: "Welcome to Healthcare Support. How can we assist you today?",
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
        // Add user message
        this.messages.push({ text: this.userInput, type: "user" });
        const inputText = this.userInput;
        this.userInput = "";

        this.$nextTick(() => {
          const chatWindow = this.$refs.chatWindow;
          chatWindow.scrollTop = chatWindow.scrollHeight;
        });

        try {
          // Send query to backend API
          const response = await axios.post("http://localhost:5000/api/query", {
            query: inputText,
          });

          const botResponse = response.data.response;
          const formattedResponse = this.formatBotResponse(botResponse);

          // Add formatted bot response
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

      // Search for the answer
      const match = pattern.exec(botResponse);
      if (match) {
        let formattedText = match[1];
        
        // Replace escape sequences with normal text
        formattedText = formattedText.replace(/\\n/g, '\n').replace(/\\"/g, '"');
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
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  font-family: "Roboto", sans-serif;
  z-index: 1000;
  transition: all 0.3s ease;
}

/* Expanded Chatbot Container */
.expanded {
  width: 700px;
  height: 600px;
}

/* Chatbot Toggle Button when closed */
.chatbot-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #004f9e;
  color: white;
  border: none;
  padding: 18px;
  border-radius: 50%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
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
  padding: 10px;
  background-color: #ffffff;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  color: #ffffff;
}

.logo {
  width: 35px;
  margin-right: 10px;
}

.chatbot-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: black;
}

/* Expand/Compress Button */
.expand-chatbot-btn {
  background-color: transparent;
  border: none;
  color: #333;
  font-size: 16px;
  cursor: pointer;
  margin-right: 10px;
}

.expand-chatbot-btn i {
  font-size: 16px;
}

/* Close Button */
.close-chatbot-btn {
  background-color: transparent;
  border: none;
  color: #333;
  font-size: 18px;
  cursor: pointer;
}

.close-chatbot-btn i {
  font-size: 18px;
}

/* Chat Window */
.chatbot-window {
  height: 350px;
  overflow-y: auto;
  padding: 15px;
  background-color: #f4f7f9;
}

.expanded .chatbot-window {
  height: 550px;
}

.message {
  padding: 10px;
  border-radius: 15px;
  max-width: 75%;
  margin-bottom: 10px;
  word-wrap: break-word;
  font-size: 14px;
}

.bot-message {
  background-color: #f0f0f0;
  color: #333333;
  align-self: flex-start;
}

.user-message {
  background-color: #004f9e;
  color: #ffffff;
  align-self: flex-end;
}

/* Input Area */
.chatbot-input-area {
  display: flex;
  padding: 15px;
  border-top: 1px solid #eeeeee;
  background-color: #ffffff;
}

.input-field {
  flex: 1;
  padding: 10px;
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
  color: #ffffff;
  padding: 10px 15px;
  border-radius: 25px;
  cursor: pointer;
  margin-left: 10px;
  display: flex;
  align-items: center;
}

.send-btn i {
  font-size: 16px;
}

.send-btn:hover {
  background-color: white;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
