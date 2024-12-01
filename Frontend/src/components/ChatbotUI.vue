<template>
  <div>
    <!-- Chatbot Toggle Button when chatbot is closed -->
    <button v-if="!isChatbotOpen" class="chatbot-toggle-btn" @click="toggleChatbot">
      <i class="fas fa-comments"></i>
    </button>

    <!-- Chatbot Panel -->
    <transition name="slide">
      <div
        v-if="isChatbotOpen"
        :class="['chatbot-container', { expanded: isExpanded }]"
        @mousedown="startDrag"
        @mousemove="onDrag"
        @mouseup="stopDrag"
        @mouseleave="stopDrag"
        :style="{ top: `${position.y}px`, left: `${position.x}px` }"
      >
        <!-- Header Section -->
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

        <!-- Chat Window Section -->
        <div class="chatbot-window" ref="chatWindow">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="messageClass(message.type)"
          >
            <div class="message" v-html="message.text"></div>
          </div>
        </div>

        <!-- Input Area Section -->
        <div class="chatbot-input-area">
          <!-- File Upload -->
          <div class="file-upload-wrapper">
            <label class="file-upload-icon">
              <input type="file" name="file" @change="handleFileUpload" hidden />
              <i class="fas fa-paperclip"></i>
            </label>
            <span v-if="fileName" class="file-name-preview">
              {{ fileName }}
              <button class="delete-file-btn" @click="deleteFile">
                <i class="fas fa-times-circle"></i>
              </button>
            </span>
          </div>

          <!-- Text Input -->
          <input
            type="text"
            v-model="userInput"
            @keydown.enter="sendMessage"
            placeholder="Type your question here..."
            class="input-field"
          />

          <!-- Send Button -->
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
      file: null,
      fileName: null,
      messages: [
        { text: "Welcome to Institute Support! How can I assist you?", type: "bot" },
      ],
      position: { x: 20, y: 20 }, // Initial draggable position
      dragging: false,
      dragStart: { x: 0, y: 0 },
    };
  },
  methods: {
    toggleChatbot() {
      this.isChatbotOpen = !this.isChatbotOpen;
    },
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
    startDrag(event) {
      this.dragging = true;
      this.dragStart = {
        x: event.clientX - this.position.x,
        y: event.clientY - this.position.y,
      };
    },
    onDrag(event) {
      if (this.dragging) {
        this.position.x = event.clientX - this.dragStart.x;
        this.position.y = event.clientY - this.dragStart.y;
      }
    },
    stopDrag() {
      this.dragging = false;
    },
    handleFileUpload(event) {
      const uploadedFile = event.target.files[0];
      if (uploadedFile) {
        this.file = uploadedFile;
        this.fileName = uploadedFile.name;
      }
    },
    deleteFile() {
      this.file = null;
      this.fileName = null;
    },
    async sendMessage() {
      if (this.userInput.trim() !== "" || this.file) {
        const formData = new FormData();
        formData.append("query", this.userInput.trim());
        formData.append("file", this.file || null);

        this.messages.push({ text: this.userInput, type: "user" });
        this.userInput = "";
        this.file = null; // Reset file input
        this.fileName = null; // Reset file name

        this.$nextTick(() => {
          const chatWindow = this.$refs.chatWindow;
          chatWindow.scrollTop = chatWindow.scrollHeight;
        });

        try {
          const response = await axios.post("http://localhost:5000/api/query", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });

          const botResponse = this.formatBotResponse(response.data.response);
          this.messages.push({ text: botResponse, type: "bot" });

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
            return `<button class="text-button" onclick="window.open('${url}', '_blank')">${url}</button>`;
          })
          .replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, (email) => {
            return `<span class="highlight">${email}</span>`;
          })
          .replace(/\b\d{2,3}\s?[-]?\s?\d{4}\s?[-]?\s?\d{4,5}\b/g, (phone) => {
            return `<span class="highlight">${phone}</span>`;
          });
        return formattedText;
      }
      return botResponse;
    },
  },
};
</script>
<style>
/* Draggable container */
.chatbot-container {
  position: absolute;
  width: 350px;
  height: 500px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: "Roboto", sans-serif;
  cursor: grab;
  z-index: 1200;
}

.chatbot-container:active {
  cursor: grabbing;
}

.expanded {
  width: 600px;
  height: 650px;
}

/* Toggle button styling */
.chatbot-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #004f9e;
  color: white;
  border: none;
  padding: 15px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  z-index: 1100;
  transition: background-color 0.3s ease;
}

.chatbot-toggle-btn:hover {
  background-color: #003d7b;
}

/* Header styling */
.chatbot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 15px;
  background-color: #004f9e;
  color: white;
}

.chatbot-header .logo {
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.chatbot-header .chatbot-title {
  flex: 1;
  font-size: 16px;
  margin-left: 10px;
  font-weight: bold;
  color: #ffffff;
}

.expand-chatbot-btn,
.close-chatbot-btn {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  margin-left: 5px;
}

.expand-chatbot-btn:hover,
.close-chatbot-btn:hover {
  color: #00b2ff;
}

/* Chat window styling */
.chatbot-window {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f4f7f9;
}

.message {
  padding: 8px 12px;
  border-radius: 12px;
  margin-bottom: 10px;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.bot-message {
  background-color: #ebf9ff;
  color: #333;
  align-self: flex-start;
}

.user-message {
  background-color: #cce5ff;
  color: #333;
  align-self: flex-end;
}

/* Input area styling */
.chatbot-input-area {
  display: flex;
  align-items: center;
  padding: 10px;
  border-top: 1px solid #ddd;
  background-color: #ffffff;
}

.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 20px;
  margin-right: 10px;
  font-size: 14px;
}

.send-btn {
  background-color: #004f9e;
  border: none;
  padding: 10px;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  font-size: 16px;
}

.send-btn:hover {
  background-color: #003d7b;
}

/* File Upload */
.file-upload-wrapper {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.file-upload-icon {
  font-size: 20px;
  color: #004f9e;
  cursor: pointer;
}

.file-name-preview {
  font-size: 12px;
  margin-left: 10px;
  color: #888;
}

.delete-file-btn {
  background: none;
  border: none;
  color: #ff5c5c;
  cursor: pointer;
  margin-left: 5px;
}

.delete-file-btn:hover {
  color: #d93838;
}

</style>