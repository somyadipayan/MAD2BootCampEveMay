<template>
    <div>
      <h2>Upload Image</h2>
      <input type="file" @change="onFileChange" />
      <button @click="uploadImage">Upload</button>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        file: null,
        message: ""
      };
    },
    methods: {
      onFileChange(event) {
        this.file = event.target.files[0];
      },
      async uploadImage() {
        if (!this.file) {
          this.message = "Please select a file.";
          return;
        }
        const formData = new FormData();
        formData.append('image', this.file);
  
        try {
          const response = await fetch('http://localhost:5000/upload-image', {
            method: 'POST',
            body: formData
          });
          const data = await response.json();
          if (response.ok) {
            this.message = "Image uploaded successfully!";
          } else {
            this.message = `Upload failed: ${data.error}`;
          }
        } catch (error) {
          this.message = `Upload failed: ${error.message}`;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add any custom styles here */
  </style>
  