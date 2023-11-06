<template>
  <main id="YipNet-MAIN">
    <NavBar id="NavBar-component-MAIN"/>
    <nav id="NavBar-space"></nav>
    <div v-if="currentView === 'LoginRegister'"><LoginRegister/></div>
    <div v-if="currentView === 'NewsFeed'"><NewsFeed/></div>
    <div v-if="currentView === 'SinglePost'"><SinglePost/></div>
    <div v-if="currentView === 'ProfileUser'"><ProfileUser/></div>
    <div v-if="currentView === 'ConfigSettings'"><ConfigSettings/></div>

    <div v-if="currentView === 'NotFound'"><NotFound/></div>

    <!-- Mostrar PostCreator solo si la sesión está activa -->
    <div v-if="sessionActive">
      <div v-if="postCreationActive"><PostCreator id="PostCreator-component-MAIN"/></div>
      <div class="post-creator-launch" @click="switchPostCreator(true)" v-else>✎</div>
    </div>
  </main>
</template>

<script>
import { ref, computed } from "vue";
import NavBar from "./components/NavBar.vue";
import LoginRegister from "./views/LoginRegister.vue";
import NewsFeed from "./views/NewsFeed.vue";
import ProfileUser from "./views/ProfileUser.vue";
import SinglePost from "./views/SinglePost.vue";
import NotFound from './views/NotFound.vue';
import PostCreator from "./components/PostCreator.vue";
import ConfigSettings from "./views/ConfigSettings.vue";
export default {
    components: {
    NavBar,
    LoginRegister,
    NewsFeed,
    ProfileUser,
    SinglePost,
    NotFound,
    PostCreator,
    ConfigSettings
},
    name: "YipNet",
    data(){
        return{
            postCreationActive: false,
            sessionActive: false
        }
    },

    methods:{
        switchPostCreator(mode_){
            this.postCreationActive = mode_;
        }
    },

    setup() {
        const currentPath = ref(window.location.hash);
        window.addEventListener("hashchange", () => {
            currentPath.value = window.location.hash;
        });

        const currentView = computed(() => {
            let route = currentPath.value.slice(2); // Elimina el '#' y el '/' del inicio de la ruta
            route = route.split("~")[0]
            if (route === "" || route === "newsfeed")
                return "NewsFeed";
            else if (route === "access")
                return "LoginRegister";
            else if (route === "post")
                return "SinglePost";
            else if (route === "profile")
                return "ProfileUser";
            else if (route === "settings")
                return "ConfigSettings";
            else return "NotFound";
        });
        return { currentView };
    },

    beforeCreate(){
        if(JSON.parse(localStorage.getItem("yipUserData")) == null)
            window.location.hash = "/access";
    },

    mounted(){
        if(JSON.parse(localStorage.getItem("yipUserData")) == null){
            this.sessionActive = false;
        }else{
            this.sessionActive = true;
        }
        console.log("Sesion activa: ", this.sessionActive)
    }

};
</script>

<style scoped>
*{
    color: white;
    font-family: sans-serif;
    color-scheme: dark !important;
}

*::-webkit-scrollbar {
    background-color: #202324;
    color: #aba499;
}

*::-webkit-scrollbar-corner {
    background-color: #181a1b;
}

*::-webkit-scrollbar-thumb {
    background-color: #454a4d;
}

#NavBar-component-MAIN{
    position: fixed;
    z-index: 10;
}

#NavBar-space{
    width: 100%;
    height: 6ch;
}

.post-creator-launch{
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5ch;
    right: 2ch;
    bottom: 2ch;
    width: 5ch;
    height: 5ch;
    border-radius: 100vw;
    position: fixed;
    background-color: blueviolet;
    z-index: 0;
    cursor: pointer;
}

#PostCreator-component-MAIN{
    z-index: 1;
}

</style>