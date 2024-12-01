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

          <!-- Microphone Button -->
          <button @click="toggleRecording" class="mic-btn">
            <i :class="isRecording ? 'fas fa-microphone-slash' : 'fas fa-microphone'"></i>
          </button>

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
      isRecording: false, // Track recording state
      recognition: null, // Speech recognition instance
      audioChunks: [], // Store audio chunks
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

    toggleRecording() {
      if (this.isRecording) {
        if (this.recognition) {
          this.recognition.stop();
        }
        this.isRecording = false;
      } else {
        this.startVoiceRecognition();
        this.isRecording = true;
      }
    },

    async startVoiceRecognition() {
      if (!("SpeechRecognition" in window || "webkitSpeechRecognition" in window)) {
        alert("Voice recognition is not supported in your browser.");
        return;
      }

      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      this.recognition = new SpeechRecognition();
      this.recognition.lang = "en-US";
      this.recognition.interimResults = false;

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        this.userInput += transcript; // Add transcribed text to userInput
      };

      this.recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
      };

      this.recognition.onend = () => {
        this.isRecording = false;
      };

      this.recognition.start();
    },

    async sendMessage() {
      if (this.userInput.trim() !== "" || this.file) {
        const formData = new FormData();
        formData.append("query", this.userInput.trim());
        if (this.file) formData.append("file", this.file);

        this.messages.push({ text: this.userInput, type: "user" });
        this.userInput = "";
        this.file = null;
        this.fileName = null;

        try {
          const response = await axios.post("http://localhost:5000/api/query", formData, {
            headers: { "Content-Type": "multipart/form-data" },
          });

          this.messages.push({ text: response.data.response, type: "bot" });
        } catch (error) {
          console.error("Error sending message:", error);
          this.messages.push({ text: "Sorry, an error occurred.", type: "bot" });
        }
      }
    },

    messageClass(type) {
      return type === "user" ? "user-message" : "bot-message";
    },
  },
};
</script>
<style>
/* Chatbot Toggle Button */
.chatbot-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}

/* Chatbot Container */
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  height: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
}

.chatbot-container.expanded {
  width: 90%;
  height: 90%;
}

/* Header Section */
.chatbot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #007bff;
  color: white;
  padding: 10px;
}

.chatbot-header .logo {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.chatbot-title {
  flex-grow: 1;
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.expand-chatbot-btn,
.close-chatbot-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 18px;
}

/* Chat Window Section */
.chatbot-window {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
}

.user-message {
  text-align: right;
}

.bot-message {
  text-align: left;
}

.message {
  display: inline-block;
  margin: 5px 0;
  padding: 10px;
  border-radius: 8px;
  background-color: #e9ecef;
  max-width: 75%;
}

.user-message .message {
  background-color: #007bff;
  color: white;
}

/* Input Area Section */
.chatbot-input-area {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #f1f1f1;
  border-top: 1px solid #ddd;
}

.input-field {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin: 0 10px;
  outline: none;
}

.send-btn,
.mic-btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 18px;
}

.mic-btn {
  margin-left: 5px;
}

.mic-btn.active {
  background-color: #dc3545;
}

/* File Upload Section */
.file-upload-wrapper {
  position: relative;
}

.file-upload-icon {
  cursor: pointer;
  color: #007bff;
  font-size: 18px;
}

.file-name-preview {
  display: flex;
  align-items: center;
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 10px;
  margin-left: 10px;
}

.delete-file-btn {
  background: none;
  border: none;
  color: #dc3545;
  font-size: 16px;
  margin-left: 5px;
  cursor: pointer;
}

/* Scrollbar Styling */
.chatbot-window::-webkit-scrollbar {
  width: 8px;
}

.chatbot-window::-webkit-scrollbar-thumb {
  background-color: #007bff;
  border-radius: 10px;
}

.chatbot-window::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

/* Transitions and Animations */
.chatbot-toggle-btn,
.chatbot-container,
.send-btn,
.mic-btn {
  transition: background-color 0.3s, transform 0.3s;
}
.chatbot-toggle-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 1100; /* Ensure it's above other elements */
}

.chatbot-toggle-btn:hover {
  transform: scale(1.1);
  background-color: #0056b3; /* Slightly darker blue on hover */
}

.chatbot-toggle-btn i {
  font-size: 24px; /* Ensure icon size is visible */
}

.chatbot-toggle-btn:hover {
  transform: scale(1.1);
}

.send-btn:hover,
.mic-btn:hover {
  transform: scale(1.2);
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s;
}

.slide-enter {
  transform: translateY(100%);
}

.slide-leave-to {
  transform: translateY(100%);
}

</style>