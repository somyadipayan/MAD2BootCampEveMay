<template>
    <NavBar />
    <div class="container mt-5">
        <h2>Update Category</h2>
        <form @submit.prevent="updateCategory">
            <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input v-model="name" type="text" class="form-control" id="name">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import UserMixin from '../mixins/userMixin';
export default {
    components: {
        NavBar
    },
    mixins: [UserMixin],
    data() {
        return {
            name: ''
        }
    },
    mounted(){
        const categoryId = this.$route.params.id
        this.fetchCategory(categoryId)
    },
    methods: {
        async updateCategory() {
            const categoryId = this.$route.params.id
            try {
                const response = await fetch(`http://localhost:5000/category/${categoryId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({
                        name: this.name
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    // PUSH TO ALL CATEGORIES
                    this.$router.push('/all-categories');

                }
                else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }

        },
        async fetchCategory(categoryId) {
            try{
                const response = await fetch(`http://localhost:5000/category/${categoryId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
                const data = await response.json();
                console.log(data)
                if (response.ok) {
                    this.name = data.name
                }
                else {
                    alert(data.error);
                }
            }
            catch(error){
                console.log(error);
            }
        }
    }
}
</script>