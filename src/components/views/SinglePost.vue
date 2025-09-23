<template>
    <main class="SinglePost-MAIN">
        <br>
        <br>
        <PostRenderer v-if="contentLoaded" :postData="content" :shared="false"/>
    </main>
</template>

<script>
import PostRenderer from '../comp/PostRenderer.vue';

export default {
    name: 'SinglePost',
    components: {
        PostRenderer,
    },
    data(){
        return{
            content: {},
            contentLoaded: false,
            postId: window.location.href.split("/").pop(),
        }
    },

    async mounted(){
        const result = await this.yipnet_GET_SINGLE_POST(this.$ENDPOINT, this.TOKEN(), this.postId);
        this.content = result || {};
        this.$nextTick(() => {
            if(result) this.contentLoaded = true;
        });
    },
}
</script>

<style scoped>
.SinglePost-MAIN h1{
    margin-top: 0;
}
</style>