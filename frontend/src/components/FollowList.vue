<template>
    <div class="FollowList-MAIN">

        <div data-aos="zoom-in">

            <button @click="hideFollowList()">+</button>

            <div class="follow-list-modes">
                <div @click="currentMode = 'followers'" :class="currentMode == 'followers' ? 'follow-active' : ''">
                    Followers
                </div>
                <div @click="currentMode = 'following'" :class="currentMode == 'following' ? 'follow-active' : ''">
                    Following
                </div>
            </div>

            <section v-if="dataExists">
                <div v-if="currentMode == 'followers'">
                    <div v-for="follower in followers" :key="follower.id">
                        <div v-if="!myBlockedList.includes(follower.id)">
                            <div @click="goToProfile(follower.id)">
                                <a :href="toProfile(follower.id)"></a>
                                <div :class="`follow-list-pfp ${follower.pfp == '' || follower.pfp == null || follower.pfp == undefined || follower.pfp.length == 0 ? 'undefined-pfp' : ''}`">
                                    <img :src="`${this.$ENDPOINT}/static/users/${follower.id}/${follower.pfp}`" alt="Profile Picture"/>
                                </div>
                                <p>{{ follower.name + " " + follower.surname }}</p>
                            </div>
                            <button v-if="!JSON.parse(follower.externalPositiveList).includes(myId)" @click="follow(follower.id)" class="BIG-BUTTON MAIN-BUTTON">Follow</button>
                            <p v-else class="following-txt">Following</p>
                            <p class="follows-you" v-if="JSON.parse(follower.positiveList).includes(myId)">Follows you</p>
                        </div>
                    </div>
                </div>

                <div v-if="currentMode == 'following'">
                    <div v-for="following in following" :key="following.id">
                        <div v-if="!myBlockedList.includes(following.id)">
                            <div @click="goToProfile(following.id)">
                                <a ::href="toProfile(following.id)"></a>
                                <div :class="`follow-list-pfp ${following.pfp == '' || following.pfp == null || following.pfp == undefined || following.pfp.length == 0 ? 'undefined-pfp' : ''}`">
                                    <img :src="`${this.$ENDPOINT}/static/users/${following.id}/${following.pfp}`" alt="Profile Picture"/>
                                </div>
                                <p>{{ following.name + " " + following.surname }}</p>
                            </div>
                            <button v-if="!JSON.parse(following.externalPositiveList).includes(myId)" @click="follow(following.id)" class="BIG-BUTTON MAIN-BUTTON">Follow</button>
                            <p v-else class="following-txt">Following</p>
                            <p class="follows-you" v-if="JSON.parse(following.positiveList).includes(myId)">Follows you</p>
                        </div>
                    </div>
                </div>
            </section>

        </div>

    </div>
</template>

<script>
export default {
    name: 'FollowList',
    props:{
        targetId: Number
    },
    data(){
        return{
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id,
            myBlockedList: JSON.parse(localStorage.getItem("yipUserData")).userData.negativeList,
            followers: [],
            following: [],
            dataExists: false,
            currentMode: "followers",
        }
    },
    methods:{
        hideFollowList(){
            this.$parent.viewFollowers(false);
        },

        getList(){
            fetch(this.$ENDPOINT+"/follow_list/" + this.targetId)
                .then(response => response.json())
                .then(data => {
                    if(data.status == "ok"){
                        this.followers = data.message.response.externalPositiveList;
                        this.following = data.message.response.positiveList;
                        this.dataExists = true;
                    }
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        },

        follow(targetId){
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/manage_follow/" + targetId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: JSON.stringify({
                    "followOrUnfollow": 1
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.status == "ok"){
                    this.getList();
                }
            })
        },

        toProfile(id_){
            const profileUrl = window.location.href.split("#")[0];
            return profileUrl + "#/profile~" + id_ ;
        },

        goToProfile(id_){
            window.location.hash = "/profile~" + id_;
            window.location.reload();
        }
    },
    mounted(){
        this.getList();
    }
}
</script>

<style scoped>
.FollowList-MAIN{
    width: 100%;
    height: calc(100vh - 6ch);
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    overflow: auto;
    left: 0;
    background-color: rgba(0, 0, 0, 0.75);
    z-index: 2;
}

.FollowList-MAIN > div{
    width: fit-content;
    height: fit-content;
    display: flex;
    flex-direction: column;
    padding: 2ch;
    border-radius: 2ch;
    background-color: rgb(52, 53, 56);
    box-shadow: 0ch 0ch 2ch rgba(0, 0, 0, 0.5);
    position: relative;
    width: 80vw;
    min-height: 50vh;
    max-height: 80vh;
    max-width: 512px;
}

.FollowList-MAIN > div > button{
    font-weight: bolder;
    width: 1ch;
    height: 1ch;
    font-size: 3ch;
    transform: rotate(45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background-color: transparent;
    border: none;
    color: gray;
    transition: all 0.1s;
    position: absolute;
    right: 1ch;
    cursor: pointer;
}

.follow-list-modes{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 3ch;
    margin-bottom: 2ch;
}

.follow-list-modes > div{
    width: 50%;
    padding: 1ch;
    border-bottom: 2px solid transparent;
    text-align: center;
    color: rgb(235, 235, 235);
}

.follow-list-modes > div:not(.follow-active):hover{
    color: white;
    border-bottom: 2px solid rgb(75, 75, 75) !important;
    cursor: pointer;
}

.follow-active{
    border-bottom: 2px solid cyan !important;
}

.follow-list-pfp{
    width: 4.5ch;
    height: 4.5ch;
    aspect-ratio: 1/1;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 100vw;
    margin-right: 1ch;
}

.follow-list-pfp:hover{
    cursor: pointer;
}

.follow-list-pfp img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    border-radius: 100vw;
}

.undefined-pfp{
    background-image: url('../assets/images/default-user.jpg') !important;
    background-position: center;
    background-size: cover;
}

.undefined-pfp img{
    display: none;
}

section{
    overflow: auto;
    height: fit-content !important;
    min-height: 100% !important;
}

section > div{
    height: fit-content;
    margin-bottom: 2px;
    position: relative;
}

section > div > div > div{
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
}

section > div > div > div > div{
    display: flex;
    align-items: center;
    height: fit-content;
}

section button{
    margin-left: 1ch;
}

.follows-you{
    position: absolute;
    color: rgb(192, 192, 192);
    left: 8.5ch;
    bottom: -1.3ch;
    font-size: 1.2ch;
    font-style: italic;
}

.following-txt{
    font-size: 1.5ch;
    color: gray;
}

section a {
    position: absolute;
    width: 75%;
    height: 80%;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    .FollowList-MAIN > div{
        width: 85vw;
        max-width: unset;
    }

}
</style>