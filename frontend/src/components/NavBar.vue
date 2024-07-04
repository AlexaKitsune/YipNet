<template>
    <nav>

        <div @click="goToNewsFeed()" class="yip-net-logo">YipNet</div>
        <div></div>
        <div v-if="userData.id">
            <div v-if="userData.id" :class="`nav-pic ${userData.currentProfilePic == '' || userData.currentProfilePic == null || userData.currentProfilePic == undefined || userData.currentProfilePic.length == 0 ? 'profile-pic-undefined' : ''}`" @click="toProfile(userData.id)">
                <img
                    :src="`${this.$ENDPOINT}/static/users/${userData.id}/${userData.currentProfilePic}`"
                    alt=""
                    :class="`updater-profile-pic `"
                >
            </div>
            <button @click="reload()"><a href="#/settings">⚙️</a></button>
        </div>

    </nav>
</template>

<script>
export default {
    name: 'NavBar',
    data(){
        return{
            userData: {}
        }
    },
    methods:{
        toProfile(id_){
            window.scrollTo(0, 0);
            window.location.hash = "#/profile~" + id_;
        },

        reload(){
            window.scrollTo(0, 0);
            event.preventDefault();
            history.pushState(null, null, '#/settings');
            window.location.reload();
        },

        goToNewsFeed(){
            window.scrollTo(0, 0);
            event.preventDefault();
            history.pushState(null, null, '#/newsfeed');
            window.location.reload();
        }
    },
    mounted(){
        try {
            this.userData = JSON.parse(localStorage.getItem("yipUserData")).userData;
        } catch (error) {
            this.userData = {}
        }
    }
}
</script>

<style scoped>
nav{
    height: 6ch;
    background-color: rgb(58, 59, 91);
    box-shadow: 0 0 1ch black;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

nav > div{
    display: flex;
    align-items: center;
    margin: 1ch;
}

.yip-net-logo{
    cursor: pointer;
}

.nav-pic, .nav-pic > div{
    width: 3.5ch;
    height: 3.5ch;
    margin-right: 1ch;
    border-radius: 100vw;
    background-size: cover;
    background-position: center;
    cursor: pointer;
    background-color: rgb(32, 33, 36);
}

.nav-pic > img{
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 100vw;
    object-fit: cover;
    object-position: center;
}

.profile-pic-undefined{
    background-image: url('../assets/images/default-user.jpg') !important;
}

.profile-pic-undefined img{
    display: none;
}

nav button{
    border: none;
    background-color: transparent;
    cursor: pointer;
    padding: 0;
    font-size: 2ch;
    width: 2.5ch;
    height: 2.5ch;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: all 0.3s;
}

nav button:hover{
    transform: rotate(45deg);
}

nav button a {
    text-decoration: none;
}
</style>