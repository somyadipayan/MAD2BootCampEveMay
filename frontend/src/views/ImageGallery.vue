<template>
    <div>
      <h2>Image Gallery</h2>
      <div v-if="images.length">
        <div v-for="image in images" :key="image.id" class="image-container">
          <img :src="`http://localhost:5000/images/${image.filename}`" :alt="image.filename" />
          <p>ID: {{ image.id }}</p>
          <p>Filename: {{ image.filename }}</p>
        </div>
      </div>
      <p v-else>No images found.</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        images: []
      };
    },
    async mounted() {
      try {
        const response = await fetch('http://localhost:5000/images');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.images = await response.json();
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    }
  };
  </script>
  
  <style scoped>
  .image-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
  }
  .image-container img {
    max-width: 100%;
    height: auto;
  }
  </style>