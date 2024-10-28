<template>
  <main id="YipNet-MAIN">
    <NavBar id="NavBar-component-MAIN"/>
    <nav id="NavBar-space"></nav>
    <div v-if="currentView === 'LoginRegister'"><LoginRegister/></div>
    <div v-if="currentView === 'NewsFeed'"><NewsFeed :key="keyComponent"/></div>
    <div v-if="currentView === 'SinglePost'"><SinglePost/></div>
    <div v-if="currentView === 'ProfileUser'"><ProfileUser :key="keyComponent"/></div>
    <div v-if="currentView === 'ConfigSettings'"><ConfigSettings/></div>
    <div v-if="currentView === 'VerifyAccount'"><VerifyAccount/></div>

    <div v-if="currentView === 'NotFound'"><NotFound/></div>

    <!-- Mostrar PostCreator solo si la sesión está activa -->
    <div v-if="sessionActive">
      <div v-if="postCreationActive"><PostCreator id="PostCreator-component-MAIN"/></div>
      <div class="post-creator-launch" @click="switchPostCreator(true)" v-else>✎</div>
    </div>
    <div class="isVerified" v-if="sessionActive && verifyAccData.verifiedAccount == 0 && verifyAccData.showVerifyAlert" data-aos="fade-up">
        <div class="close-verify" @click="verifyAccData.showVerifyAlert = false">+</div>
        <p>
            <b>A verification email has been sent to your email address.</b><br>
            Your account and all associated information will be deleted in 72 hours (<b>{{verifyAccData.countdown}}</b>) if you do not verify your email.
        </p>
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
import VerifyAccount from './views/VerifyAccount.vue';
import AOS from 'aos';
import 'aos/dist/aos.css';
export default {
    components: {
    NavBar,
    LoginRegister,
    NewsFeed,
    ProfileUser,
    SinglePost,
    NotFound,
    PostCreator,
    ConfigSettings,
    VerifyAccount,
},
    name: "YipNet",
    data(){
        return{
            postCreationActive: false,
            sessionActive: false,
            keyComponent: 0,
            verifyAccData: {           
                verifiedAccount: 0,
                showVerifyAlert: true,
                registrationDate: "",
                countdown: "",
            }
        }
    },

    methods:{
        switchPostCreator(mode_){
            this.postCreationActive = mode_;
        },

        changeKeyComponent(){
            this.keyComponent++;
        },

        startCountdown() {
            const registrationDate = new Date(this.verifyAccData.registrationDate);
            const endTime = new Date(registrationDate.getTime() + 72 * 60 * 60 * 1000); // 72 hours later

            const updateCountdown = () => {
                const now = new Date();
                const timeRemaining = endTime - now;

                if (timeRemaining > 0) {
                    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((timeRemaining / (1000 * 60 * 60)) % 24);
                    const minutes = Math.floor((timeRemaining / (1000 * 60)) % 60);
                    const seconds = Math.floor((timeRemaining / 1000) % 60);

                    this.verifyAccData.countdown = `${days}d ${hours}h ${minutes}m ${seconds}s`;
                } else {
                    this.verifyAccData.countdown = "Expired";
                }
            };

            updateCountdown();
            setInterval(updateCountdown, 1000);
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
            else if (route === "verify")
                return "VerifyAccount";
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
            const yipUserData = JSON.parse(localStorage.getItem("yipUserData"));
            this.verifyAccData.verifiedAccount = parseInt(yipUserData.userData.verified);
            this.verifyAccData.registrationDate = yipUserData.userData.registrationDate;
            if(this.verifyAccData.verifiedAccount == 0){
                this.startCountdown();
            }
        }
        console.log("Sesion activa: ", this.sessionActive);
        AOS.init();
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


.isVerified{
    border-radius: 1ch;
    position: fixed;
    top: 7ch;
    padding: 0.5ch;
    background-color: #FDF5C7;
    border: 2px solid #d48702;
    width: 95%;
    margin-left: calc((5%/2) - 8px);
}

.isVerified p, .isVerified b{
    margin: 0;
    color: #d48702;
}

.isVerified > p > b:nth-child(1){
    color: inherit;
    text-transform: uppercase;
}

.close-verify{
    color: #d48702;
    position: absolute;
    top: 0.4ch;
    right: 0.4ch;
    width: 1ch;
    height: 1ch;
    font-size: 3ch;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    rotate: 45deg;
    cursor: pointer;
}
</style>