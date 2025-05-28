<template>
    <main class="NewsFeed-MAIN">
        
        <br><br>
        
        <!-- post list -->
        <section v-for="(item, index) in newsfeedPosts" :key="index" style="overflow: hidden;">
            <PostRenderer :postData="item" :shared="false"/>
        </section>

    </main>
</template>

<script>
import PostRenderer from '../comp/PostRenderer.vue';

export default{
    name: 'NewsFeed',
    components: {
        PostRenderer
    },
    data(){
        return{
            AlexiconUserData: {},
            newsfeedPosts: [],
        }
    },
    methods: {
        newsfeed(){
            const token = this.AlexiconUserData.token;

            fetch(this.$ENDPOINT+"/yipnet/newsfeed", {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(res => res.json())
            .then(data => {
                console.log("Newsfeed:", data);
                this.newsfeedPosts = data.response;
            })
            .catch(err => {
                console.error("Error al recuperar newsfeed:", err);
            });
        }
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.newsfeed();
    }
}
</script>

<style scoped>
.NewsFeed-MAIN{

}
</style>