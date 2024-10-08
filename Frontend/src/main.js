import { createApp } from 'vue';
import App from './App.vue';
// import router from './router'; // Import the router
import '@fortawesome/fontawesome-free/css/all.css';


const app = createApp(App);

// app.use(router); // Add the router to the Vue app

app.mount('#app');
