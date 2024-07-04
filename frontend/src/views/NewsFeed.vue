<template>
    <main>
        <!--Newsfeed-->

        <section class="newsfeed-posts">
            <PostViewer v-for="post in postList" :key="post.id" :postData="post"/>
        </section>

    </main>
</template>

<script>
import PostViewer from '@/components/PostViewer.vue';
export default {
    components: { PostViewer },
    name: 'NewsFeed',
    data(){
        return{
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id,
            postList: [],
        }
    },
    methods: {
        getNewsFeed(){
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/news_feed/" + this.myId, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + token // Donde "token" es el token de autorización que deseas enviar
                }})
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    if(data.message)
                        this.postList = data.message.response;
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        }
    },
    beforeCreate(){
        if(JSON.parse(localStorage.getItem("yipUserData"))  == null)
            window.location.hash = "/access";
    },
    mounted(){
        this.getNewsFeed();
    }
}
</script>

<style scoped>
.newsfeed-posts{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

</style>