<template>
    <main>
        <PostViewer v-if="isObject(postData)" :postData="postData"/>
    </main>
</template>

<script>
import PostViewer from '@/components/PostViewer.vue';

export default {
    name: 'SinglePost',
    components: { PostViewer },
    data(){
        return{
            postData: Object
        }
    },
    methods:{
        isObject(value) {
            return typeof value === 'object' && value !== null;
        },

        getPostInfo(){
            let postId = window.location.href.split("~")[1];
            postId = parseInt(postId);
            console.log(postId);

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/single_post/" + postId, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                })
                .then(response => response.json())
                .then(data => {
                    this.postData = data.message;
                    console.log("data:", this.postData);
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        }
    },

    mounted(){
        this.getPostInfo();
    }
}
</script>

<style scoped>
main{
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>