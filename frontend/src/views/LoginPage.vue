<template>

<div class="container">
<h2>Login Here</h2>
<form @submit.prevent="login">
  <div class="mb-3">
    <label for="email" class="form-label">Email address</label>
    <input v-model="email" type="email" class="form-control" id="email">
  </div>
  <div class="mb-3">
    <label for="password" class="form-label">Password</label>
    <input v-model="password" type="password" class="form-control" id="password">
  </div>
  <button type="submit" class="btn btn-primary">Login</button>
</form>
</div>

</template>

<script>
export default{
    data() {
        return {
            email: '',
            password: ''
        }
    },
    methods: {
        async login(){
            try{
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password,
                })
            })
            const data = await response.json();
            console.log(data)
            if(response.ok){
                console.log(data.message);
                localStorage.setItem("access_token", data.access_token);
                alert(data.message)
                this.$router.push('/')
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

<style scoped></style>