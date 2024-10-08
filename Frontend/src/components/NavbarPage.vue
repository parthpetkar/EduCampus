<template>
    <nav class="navbar">
        <img src = "@/assets/logo1.png" class="logo"/>
      <ul>
        <li><a href="/">HOME</a></li>
        <li><a href="#">ALUMNI</a></li>
        <li><a href="#">CONTACT</a></li>
        <li><a href="#">AICTE APPROVAL</a></li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavbarPage'
  }
  </script>
  
  <style scoped>
  .logo{
    height: 29%;
    width: 29%;
    align-items: center;
    justify-content: center;
    
  }
  .navbar {
    background-color: white; /* Primary blue color */
    color: black;
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    width: 98%;
    z-index: 1000;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .navbar h1 {
    margin: 0;
  }
  
  .navbar ul {
    list-style: none;
    padding: 0;
    display: flex;
    margin-right: 50px;
    gap: 1.5rem;
  }
  
  .navbar ul li {
    display: inline-block;
  }
  
  .navbar a {
    color: goldenrod;
    text-decoration: none;
    /* font-weight: bold; */
  }
  
  .navbar a:hover {
    text-decoration: underline;
    color: black;
  }
  </style>
  