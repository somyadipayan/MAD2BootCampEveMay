<template>
  <NavBar/>
<div class="container">
<h2>Register Here</h2>
<form @submit.prevent="register">
  <div class="mb-3">
    <label for="email" class="form-label">Email address</label>
    <input v-model="email" type="email" class="form-control" aria-describedby="emailHelp" id="email">
    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
  </div>
  <div class="mb-3">
    <label for="name" class="form-label">Name</label>
    <input v-model="name" type="text" class="form-control" id="name">
  </div>
  <div class="mb-3">
    <label for="city" class="form-label">City</label>
    <input v-model="city" type="text" class="form-control" id="city">
  </div>
  <div class="mb-3">
    <label for="password" class="form-label">Password</label>
    <input v-model="password" type="password" class="form-control" id="password">
  </div>
  <div class="mb-3 form-check">
    <input v-model="isManager" type="checkbox" class="form-check-input" id="isManager">
    <label class="form-check-label" for="isManager">Do you want to register as Manager?</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
</div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    components: {
        NavBar
    },
    data(){
        return {
            email: '',
            name: '',
            city: '',
            password: '',
            isManager: false
        }
    },
    methods: {
        async register(){
            try{
            const response = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    name: this.name,
                    city: this.city,
                    password: this.password,
                    role: this.isManager ? "manager" : "user"
                })
            })
            const data = await response.json();
            if(response.ok){
                console.log(data.message);
                alert(data.message)
                this.$router.push('/login')
            } else {
                console.log(data.error);
                alert(data.error)
            }
        }
        catch(error){
            console.log(error);
            alert(error)
        }
    }
    }
}

</script>

<style scoped>

</style>