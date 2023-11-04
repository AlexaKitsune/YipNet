<template>
    <main>
        Newsfeed
    </main>
</template>

<script>
export default {
    name: 'NewsFeed',
    
    beforeCreate(){
        if(JSON.parse(localStorage.getItem("yipUserData"))  == null)
            window.location.hash = "/access";
    }
}
</script>

<style scoped>

</style>