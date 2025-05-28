<template>
    <section class="MessageRenderer-MAIN">
        {{ messageData }}
    </section>
</template>

<script>
export default {
    name: 'MessageRenderer',
    props: {
        messageData: Object,
    },
    data(){
        return{
            AlexiconUserData: {},
        }
    },
    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
    }
}
</script>

<style scoped>
.MessageRenderer-MAIN{
    border: 1px solid red;
}
</style>