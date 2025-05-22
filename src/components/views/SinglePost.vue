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
            AlexiconUserData: {},
            postId: 0,
            content: {},
            contentLoaded: false,
        }
    },

    methods: {
        getPostId(){
			const path = new URL(window.location.href).pathname;
			let pathArray = path.split("/");
			// eslint-disable-next-line
			let x = pathArray.shift();
			this.postId = pathArray[1];
        },

        getSinlgePost(id_){
            const token = this.AlexiconUserData.token;
            const headers = {
                "Content-Type": "application/json"
            };
            if (token) {
                headers["Authorization"] = `Bearer ${token}`;
            }

            fetch(this.$ENDPOINT+`/yipnet/get_single_post?id=${id_}`, {
                    method: "GET",
                    headers: headers
                })
                .then(res => res.json())
                .then(data => {
                    if (data.response) {
                        console.error("Error del servidor:", data.response);
                    } else {
                        console.log("Post recibido:", data);
                        this.content = data;
                        this.$nextTick(() => {
                            this.contentLoaded = true;
                        });
                    }
                })
                .catch(err => {
                    console.error("Error de red o servidor:", err);
                });
        }
    },

    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.getPostId();
        this.getSinlgePost(this.postId);
    }
}
</script>

<style scoped>
.SinglePost-MAIN h1{
    margin-top: 0;
}
</style>