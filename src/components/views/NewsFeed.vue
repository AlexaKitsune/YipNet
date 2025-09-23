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
            newsfeedPosts: [],
        }
    },
    async mounted(){
        const result = await this.yipnet_NEWSFEED(this.$ENDPOINT, this.TOKEN());
        this.newsfeedPosts = result?.response ?? [];
    }
}
</script>