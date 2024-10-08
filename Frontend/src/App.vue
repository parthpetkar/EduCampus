<template>
  <div id="app">
    <NavbarPage />
    <div class="golden-bar"></div> <!-- Golden bar -->
    <div class="main-content">
      <Chatbot /> <!-- Chatbot added here -->
    </div>
    <FooterPage />
  </div>
</template>

<script>
import NavbarPage from './components/NavbarPage.vue';
import FooterPage from './components/FooterPage.vue';
import Chatbot from './components/ChatbotUI.vue';

export default {
  components: {
    NavbarPage,
    FooterPage,
    Chatbot
  }
}
</script>

<style scoped>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #f4f7fc;
}

.main-content {
  display: flex;
  flex-direction: column; /* Add this to ensure correct vertical layout */
  min-height: calc(100vh - 100px);
}

.golden-bar {
  background-color: gold; /* Golden color */
  height: 5px; 
  width: 100%; 
  z-index: 99;
}

.logotp {
  margin-top: 50px;
}

.tpss {
  font-size: 120px;
}

body {
  margin: 0;
  padding: 0;
}
</style>
