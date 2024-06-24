<template>
    <NavBar />
    <div class="container mt-4">
        <h2>All Categories</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Created By</th>
                    <th scope="col">Name</th>
                    <th  v-if="this.role === 'admin'" scope="col">Status</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for= "category in categories" :key="category.id">
                    <th scope="row">{{category.id}}</th>
                    <td>{{ category.creator_email }}</td>
                    <td>{{category.name}}</td>
                    <td  v-if="this.role === 'admin'">
                        <button v-if="!category.verified" class="btn btn-light" @click="verifyCategory(category.id)">Verify</button>
                        <button v-else class="btn btn-light" disabled>Verified</button>
                    </td>
                    <td class="btn-group">
                        <router-link v-if="this.role === 'admin' || this.role === 'manager'" :to="`/update-category/${category.id}`" class="btn btn-light">Update</router-link>
                        <button v-if="this.role === 'admin'" class="btn btn-light" @click="deleteCategory(category.id)">Delete</button>
                        <button class="btn btn-light" @click="viewCategory(category.id)">View</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <router-link to="/add-category" class="btn btn-dark">Add Category</router-link>

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
            categories: []
        }
    },
    created() {
        this.getCategories();
    },
    methods: {
        async getCategories() {
            try {
                const response = await fetch('http://localhost:5000/categories',{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                const data = await response.json();
                if(response.ok){
                    this.categories = data.categories;
                } else {
                    alert("Something went wrong");
                }
            } catch (error) {
                console.log(error);
            }
        },

        async deleteCategory(id) {
            try {
                const response = await fetch(`http://localhost:5000/category/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                const data = await response.json();
                if(response.ok){
                    alert(data.message);
                    this.getCategories();
                } else {
                    alert(data.error);
                }
            } catch (error) {
                console.log(error);
            }
        },
        viewCategory(id) {
            console.log('Viewing category: ', id);
        },
        async verifyCategory(id) {
            try {
                const response = fetch(`http://localhost:5000/verify-category/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
                });
                const data = await response.json();
                if (response.ok) {
                    console.log(data.message);
                    alert(data.message);
                    this.getAllCategories();
                } else {
                    console.log(data.error);
                    alert(data.error);
                }
            } catch (error) {
                console.error(error);
            }
        }
    }
}
</script>
