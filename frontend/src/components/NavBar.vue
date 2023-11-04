<template>
    <nav>

        <div>*</div>
        <div></div>
        <div v-if="userData.id">
            <div v-if="userData.id" class="nav-pic" @click="toProfile(userData.id)">
                <div :style="`background-image:url('${this.$ENDPOINT}/static/users/${userData.id}/${userData.currentProfilePic}');`"></div>
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
            window.location.hash = "#/profile~" + id_;
        },

        reload(){
            event.preventDefault();
            history.pushState(null, null, '#/settings');
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

.nav-pic, .nav-pic > div{
    width: 3.5ch;
    height: 3.5ch;
    margin-right: 1ch;
    border-radius: 100vw;
    background-size: cover;
    background-position: center;
    cursor: pointer;
    background-image: url('../assets/images/default-user.jpg');
}

.nav-pic > div{
    position: relative;
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