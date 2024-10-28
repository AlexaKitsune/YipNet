<template>
    <main class="ProfileUser-MAIN">

        <div class="profile-cover"><!--Portada cargada en background-image:url()-->
            <div class="profile-cover-img">
                <div :style="`background-image:url('${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentCoverPic}');`" class="sub-cover-pic updater-cover-pic"></div>
                <button class="profile-change-cover" v-if="profileData.id == myId" @click="updatePics(true, 'cover')">📷</button>
            </div>
            <div class="profile-pic">
                <img
                    ref="profilePic"
                    :src="`${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentProfilePic}`"
                    :class="`profile-pic sub-profile-pic updater-profile-pic ${profileData.currentProfilePic == '' || profileData.currentProfilePic == null || profileData.currentProfilePic == undefined || profileData.currentProfilePic.length == 0 ? 'profile-pic-undefined' : ''}`"
                >
                <button class="profile-change-pic" v-if="profileData.id == myId" @click="updatePics(true, 'profile')">📷</button>
            </div><!--Imagen de perfil-->
        </div>

        <div class="profile-info">
            <div>
                <h1>{{ profileData.name  +" "+ profileData.surname }}   </h1>
                <!--<p class="profile-arroba">@</p>-->
                <p>
                    <span v-if="target.description">{{ target.description }}</span>
                    <span v-else class="no-description">Add description.</span>
                </p>
            </div>
            <div class="profile-follow-info">
                <div v-if="myId != targetId">
                    <button v-if="!checkIfIncludes(target.externalPositiveList, myId)" class="BIG-BUTTON MAIN-BUTTON" @click="manageFollow(true)">Follow</button>
                    <button v-if="checkIfIncludes(target.externalPositiveList, myId)" class="BIG-BUTTON MAIN-BUTTON" @click="manageFollow(false)">Unfollow</button>
                    <button class="BIG-BUTTON MAIN-BUTTON profile-block" @click="blockAlert = true">Block</button>
                </div>
                <div class="follow-info" @click="showFollowList = true">
                    <div><b>{{ target.externalPositiveList?.length }}</b> &nbsp; Followers</div>
                    <div><b>{{ target.positiveList?.length }}</b> &nbsp; Following</div>
                </div>
            </div>
        </div>

        <section class="update-pics" ref="updatePics" v-if="updatePicsShow">
            <div data-aos="zoom-in">
                <button @click="updatePics(false)">+</button>
                <p ref="updateWhat"></p>
                <div class="update-pics-area">
                    <div v-if="imageToUpdate === 'cover'" class="update-pic-cover" 
                        :style="imageFileToUpdate == '' ? `background-image:url('${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentCoverPic}'); opacity: 0.5;` : `background-image: url(${imageFileToUpdate});`
                    "></div>
                    <div v-if="imageToUpdate === 'profile'" class="update-pic-profile" 
                        :style="imageFileToUpdate == '' ? `background-image:url('${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentProfilePic}'); opacity: 0.5;` : `background-image: url(${imageFileToUpdate});`
                    "></div>
                    <input type="file" @change="handleImageUpload" name="media" accept="image/*" ref="inputImageToUpload">
                </div>
                <div class="update-pics-buttons">
                    <button class="SECONDARY-BUTTON" ref="updatePicUpload" @click="uploadPic()">Upload</button>
                    <button class="SECONDARY-BUTTON" @click="updatePics(false)">Cancel</button>
                </div>
            </div>
        </section>

        <FollowList v-if="showFollowList" :targetId="targetId"/>

        <section class="block-section" v-if="blockAlert">
            <div>
                <button @click="blockAlert = false">+</button>
                <div class="profile-pic block-pic">
                    <img
                        :src="`${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentProfilePic}`"
                        :class="`profile-pic sub-profile-pic updater-profile-pic ${profileData.currentProfilePic == '' || profileData.currentProfilePic == null || profileData.currentProfilePic == undefined || profileData.currentProfilePic.length == 0 ? 'profile-pic-undefined' : ''}`"
                    >
                    <button class="profile-change-pic" v-if="profileData.id == myId" @click="updatePics(true, 'profile')">📷</button>
                </div>
                <h1>Are you sure you want to block {{ profileData.name }}?</h1>
                <div>
                    <button class="BIG-BUTTON MAIN-BUTTON profile-block" @click="manageBlock()">Block</button>
                    <button class="BIG-BUTTON MAIN-BUTTON" @click="blockAlert = false">Cancel</button>
                </div>
            </div>

        </section>
        
        <section class="profile-posts">
            <PostViewer v-for="post in postList" :key="post.id" :postData="post"/>
        </section>

    </main>
</template>

<script>
import PostViewer from '@/components/PostViewer.vue';
import FollowList from '@/components/FollowList.vue';

export default {
    name: 'ProfileUser',
    components: { PostViewer, FollowList },
    data(){
        return{
            profileData: Object,
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id,
            postList: [],
            imageToUpdate: '',
            imageFileToUpdate: '',
            targetId: 0,
            myPositiveList: [],
            target:{
                externalPositiveList: [],
                positiveList: [],
                description: false,
            },
            showFollowList: false,
            blockAlert: false,
            updatePicsShow: false,
        }
    },

    methods:{
        getUser(){
            let userId = window.location.href.split("~")[1];
            userId = parseInt(userId);
            this.targetId = userId;
            const myBlockedList = JSON.parse(localStorage.getItem("yipUserData")).userData.negativeList;
            const myExternalNegativeList = JSON.parse(localStorage.getItem('yipUserData')).userData.externalNegativeList;
            if(myBlockedList.includes(this.targetId) || myExternalNegativeList.includes(this.targetId)){
                window.location.hash = "/NotFound";
                return;
            }

            if(!isNaN(userId)){
                fetch(this.$ENDPOINT+"/profile/" + userId)
                    .then(response => response.json())
                    .then(data => {
                        console.log("selected data:")
                        console.log("all data", data)
                        this.profileData = data.message;
                        this.target.positiveList = this.profileData.positiveList;
                        this.target.externalPositiveList = this.profileData.externalPositiveList;
                        this.target.description = data.message.description;
                    })
                    .catch(error => {
                        console.error("Error: ", error);
                    });

                const token = JSON.parse(localStorage.getItem("yipUserData")).token;
                fetch(this.$ENDPOINT+"/post_list/" + userId, {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Bearer ' + token // Donde "token" es el token de autorización que deseas enviar
                    }})
                    .then(response => response.json())
                    .then(data => {
                        if(data.message)
                            this.postList = data.message.post_list;
                    })
                    .catch(error => {
                        console.error("Error: ", error);
                    });
            }
        },

        updatePics(show_, pic_){
            this.updatePicsShow = show_;
            this.imageToUpdate = pic_;
            
            this.$nextTick(() => {
                if(show_) this.$refs.updateWhat.textContent = pic_ == "cover" ? "Update cover image" : "Update profile picture";
            });
        },

        handleImageUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const imageUrl = e.target.result;
                    this.imageFileToUpdate = imageUrl;
                };
                reader.readAsDataURL(file);
                this.$refs.updatePicUpload.className = "MAIN-BUTTON";
            }
        },

        uploadPic() {
            if (this.imageFileToUpdate === '') {
                return;
            }

            // Crea un objeto FormData y agrega la imagen
            const formData = new FormData();
            formData.append("media", this.$refs.inputImageToUpload.files[0]);
            console.log(this.imageFileToUpdate)

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT + "/update_pic/" + this.imageToUpdate, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    body: formData, // Usa el objeto FormData para enviar la imagen
                })
                .then(response => response.json())
                .then(data => {
                    if(data.status == "ok"){
                        let yipUserData = JSON.parse(localStorage.getItem("yipUserData"));
                        if(this.imageToUpdate == "profile"){
                            yipUserData.userData.currentProfilePic = data.message.image_added;
                            document.querySelectorAll(".updater-profile-pic").forEach(pic => { 
                                pic.style.backgroundImage = `url(${this.$ENDPOINT}/static/users/${this.profileData.id}/${data.message.image_added})`;
                                pic.src = `${this.$ENDPOINT}/static/users/${this.profileData.id}/${data.message.image_added}`;
                            });
                            this.$refs.profilePic.src = `${this.$ENDPOINT}/static/users/${this.profileData.id}/${data.message.image_added}`;
                        }else{
                            yipUserData.userData.currentCoverPic = data.message.image_added;
                            document.querySelectorAll(".updater-cover-pic").forEach(pic => { 
                                pic.style.backgroundImage = `url(${this.$ENDPOINT}/static/users/${this.profileData.id}/${data.message.image_added})`;
                            });
                        }
                        localStorage.setItem("yipUserData", JSON.stringify(yipUserData));
                        this.updatePics(false);
                    }
                })
                .catch(error => {
                    console.error('Error en la carga de la imagen:', error);
                });
        },

        manageFollow(followOrUnfollow_){
            console.log(followOrUnfollow_);
            console.log(this.myId);
            console.log(this.targetId);

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/manage_follow/" + this.targetId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: JSON.stringify({
                    "followOrUnfollow": followOrUnfollow_ ? 1 : 0
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.status == "ok"){
                    if(followOrUnfollow_){
                        if (!this.target.externalPositiveList.includes(this.myId)) {
                            this.target.externalPositiveList.push(this.myId);
                        }
                    }else{
                        const index = this.target.externalPositiveList.indexOf(this.myId);
                        if (index !== -1) {
                            this.target.externalPositiveList.splice(index, 1);
                        }
                    }
                }
            })
        },

        checkIfIncludes(arr_, element_){
            return arr_.includes(element_)
        },

        viewFollowers(mode_){
            this.showFollowList = mode_;
            console.log(this.showFollowList)
        },

        manageBlock(){
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/manage_block/" + this.targetId, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: JSON.stringify({
                    "blockOrUnblock": 1
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.status == "ok"){
                    let yipUserData = JSON.parse(localStorage.getItem("yipUserData"));
                    console.log("blocked", data.message.target_user);

                    if(!yipUserData.userData.negativeList.includes(data.message.target_user)){
                        let negativeList;
                        if(typeof yipUserData.userData.negativeList == "string"){
                            negativeList = JSON.parse(yipUserData.userData.negativeList);
                        }else{
                            negativeList = yipUserData.userData.negativeList;
                        }

                        console.log(negativeList)
                        negativeList.push(data.message.target_user);
                        yipUserData.userData.negativeList = negativeList;
                    }

                    localStorage.setItem("yipUserData", JSON.stringify(yipUserData));

                    window.location.hash = "/newsfeed";
                    window.location.reload();
                }
            })
        },
    },

    beforeCreate(){
        if(JSON.parse(localStorage.getItem("yipUserData"))  == null)
            window.location.hash = "/access";
    },

    mounted(){
        this.getUser();
        this.hashChangeHandler = () => {
            this.getUser();
        };
        window.addEventListener("hashchange", this.hashChangeHandler);
        
    },

    // Asegúrate de eliminar el listener cuando el componente se destruye
    beforeUnmount() {
        window.removeEventListener("hashchange", this.hashChangeHandler);
    },

}
</script>

<style scoped>
.ProfileUser-MAIN{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.profile-cover{
    width: 100%;
    height: 40vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    clip-path: inset(0 0 0 0);
}

.profile-cover-img, .profile-cover-img > div{
    width: inherit;
    height: inherit;
    background-size: cover;
    background-position: center;
    background-image: url('../assets/images/default-cover.jpg');
    position: fixed;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
}

.profile-cover-img > div{
    position: absolute;
}

.profile-pic, .profile-pic > img{
    position: absolute;
    width: 20vh;
    height: 20vh;
    border-radius: 100vw;
    background-size: cover;
    background-position: center;
    border: 5px solid rgb(32, 33, 36);
    display: flex;
    align-items: flex-end;
    justify-content: center;
    object-fit: cover;
    object-position: center;
    background-color: rgb(32, 33, 36);
}

.profile-pic-undefined{
    background-image: url('../assets/images/default-user.jpg') !important;
}

.profile-pic > img{
    width: inherit;
    height: inherit;
    border: none;
    position: absolute;
}

.profile-cover-img > button, .profile-pic > button{
    margin-right: 2ch;
    font-size: 2ch;
    background-color: transparent;
    border: none;
    cursor: pointer;
}

.profile-pic > button{
    margin: unset;
}

.profile-info {
    margin-top: 1ch;
    padding: 1ch 3ch;
    display: flex;
}

.profile-info > *{
    margin: 0;
}

.profile-info > div{
    display: flex;
    flex-direction: column;
    height: fit-content;
}

.profile-info > div:nth-child(1){
    text-align: left;
    width: 100%;
}

.profile-info > div:nth-child(2){
    text-align: right;
    width: fit-content;
}

.profile-info > div > *{
    height: fit-content;
    margin: 0;
}

.profile-info p{
    margin-top: 1ch;
}

.no-description{
    color: gray;
}

.profile-info button{
    border: none;
    border-radius: 0.5ch;
    margin:  0 1ch;
    cursor: pointer;
}

.profile-follow-info button{
    margin-right: 0;
    margin-bottom: 1.5ch;
}

.profile-follow-info div:not(.follow-info){
    display: flex !important;
    flex-direction: row !important;
    white-space: nowrap;
    color: rgb(182, 182, 182);
    width: 100%;
}

.follow-info{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

.follow-info > div{
    width: fit-content !important;
}

.follow-info:hover, .follow-info:hover *{
    cursor: pointer;
    color: rgb(222, 222, 222) !important;
}

.profile-block{
    color: orange;
}

.profile-block:hover{
    background-color: red;
    color:  white;
}

.profile-arroba{
    color: lightgray;
}

.profile-posts{
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.sub-profile-pic, .sub-cover-pic{
    pointer-events: none;
    z-index: 1;
}

/* Update data */
.profile-change-pic, .profile-change-cover{
    z-index: 2;
}

.profile-change-pic:hover, .profile-change-cover:hover{
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 1ch;
}

.update-pics, .block-section{
    width: 100%;
    height: calc(100vh - 6ch);
    display: flex;
    display: none;
    align-items: center;
    justify-content: center;
    position: fixed;
    overflow: auto;
    left: 0;
    background-color: rgba(0, 0, 0, 0.75);
}

.update-pics{
    z-index: 2;
    display: flex;
}

.block-section{
    display: flex;
}

.update-pics p{
    margin-bottom: 3ch;
}

.update-pics > div, .block-section > div{
    width: fit-content;
    height: fit-content;
    display: flex;
    flex-direction: column;
    padding: 2ch;
    border-radius: 2ch;
    background-color: rgb(52, 53, 56);
    box-shadow: 0ch 0ch 2ch rgba(0, 0, 0, 0.5);
    position: relative;
}

.block-section{
    z-index: 2;
}

.block-section > div{
    align-items: center;
    max-width: 80%;
    margin-top: -3ch;
}

.update-pics > div > button, .block-section > div > button{
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
}

.update-pics > div > button:hover, .block-section > div > button:hover{
    cursor: pointer;
    scale: 1.1;
}

.update-pics > div > button:hover{
    cursor: pointer;
    color: lightgray;
    transition: all 0.2s;
}

.update-pics-area {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.update-pics-area > div{
    border: 2px solid gray;
    margin-bottom: 3ch;
}

.update-pics-area > input{
    position: absolute;
    width: 100%;
    height: calc(100% - 3ch);
    margin-bottom: 3ch;
    opacity: 0;
    cursor: crosshair;
}

.update-pic-cover{
    width: 48ch;
    height: 24ch;
    border-radius: 1ch;
    background-position: center;
    background-size: cover;
}

.update-pic-profile{
    width: 30ch;
    height: 30ch;
    border-radius: 100vw;
    background-position: center;
    background-size: cover;
}

.update-pics-buttons{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.update-pics-buttons > button{
    border: none;
    padding: 0.5ch;
    border-radius: 0.5ch;
}

.block-pic{
    position: relative;
    top: unset;
    left: unset;
    right: unset;
    bottom: unset;
    margin: unset;
    width: 10ch !important;
    height: 10ch !important;
}

.block-section > div > div{
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}
/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    .ProfileUser-MAIN{
        margin: 0;
        overflow-x: hidden;
        max-width: 100vw;
    }

    .profile-cover{
        width: 100vw;
        height: 50vw;
    }

    .profile-pic{
        width: 33vw;
        height: 33vw;
    }

    .update-pic-cover{
        width: 75vw;
        height: 40vw;
    }

    .update-pic-profile{
        width: 60vw;
        height: 60vw;
    }

    .profile-info{
        flex-direction: column;
    }

    .profile-follow-info{
        width: 100% !important;
        max-width: unset;
        display: flex;
        align-items: center !important;
        justify-content: space-between;
        flex-direction: row-reverse !important;
        margin-top: 2.2ch;
    }

    .profile-follow-info div:not(.follow-info){
        width: fit-content;
        align-self: unset;
        display: flex;
    }

    .follow-info{
        align-items: flex-start;
    }

    .profile-follow-info button{
        margin-bottom: 0;
    }

}
</style>