<template>
    <main class="ProfileUser-MAIN">

        <div class="profile-cover"><!--Portada cargada en background-image:url()-->
            <div class="profile-cover-img">
                <div :style="`background-image:url('${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentCoverPic}');`" class="sub-cover-pic updater-cover-pic"></div>
                <button class="profile-change-cover" v-if="profileData.id == myId" @click="updatePics(true, 'cover')">📷</button>
            </div>
            <div class="profile-pic">
                <div :style="`background-image:url('${this.$ENDPOINT}/static/users/${profileData.id}/${profileData.currentProfilePic}');`" class="profile-pic sub-profile-pic updater-profile-pic"></div>
                <button class="profile-change-pic" v-if="profileData.id == myId" @click="updatePics(true, 'profile')">📷</button>
            </div><!--Imagen de perfil-->
        </div>

        <div class="profile-info">
            <div>
                <h1>{{ profileData.name  +" "+ profileData.surname }}   </h1>
                <p class="profile-arroba">@</p>
                <p>
                    <span v-if="description">{{ description }}</span>
                    <span v-else class="no-description">Add description.</span>
                </p>
            </div>
            <div>
                0
            </div>
        </div>

        <section class="profile-posts">
            <PostViewer v-for="post in postList" :key="post.id" :postData="post" />
        </section>

        <section class="update-pics" ref="updatePics">
            <div>
                <button @click="updatePics(false)">+</button>
                <p ref="updateWhat"></p>
                <div class="update-pics-area">
                    <div v-if="imageToUpdate === 'cover'" class="update-pic-cover" :style="{ 'background-image': 'url(' + imageFileToUpdate + ')' }"></div>
                    <div v-if="imageToUpdate === 'profile'" class="update-pic-profile" :style="{ 'background-image': 'url(' + imageFileToUpdate + ')' }"></div>
                    <input type="file" @change="handleImageUpload" name="media" accept="image/*" ref="inputImageToUpload">
                </div>
                <div class="update-pics-buttons">
                    <button class="SECONDARY-BUTTON" ref="updatePicUpload" @click="uploadPic()">Upload</button>
                    <button class="SECONDARY-BUTTON" @click="updatePics(false)">Cancel</button>
                </div>
            </div>
        </section>
        
    </main>
</template>

<script>
import PostViewer from '@/components/PostViewer.vue';

export default {
    name: 'ProfileUser',
    components: { PostViewer },
    data(){
        return{
            profileData: Object,
            myId: JSON.parse(localStorage.getItem("yipUserData")).userData.id,
            postList: [],
            imageToUpdate: '',
            imageFileToUpdate: ''
        }
    },

    methods:{
        getUser(){
            let userId = window.location.href.split("~")[1];
            userId = parseInt(userId);
            console.log(userId)

            if(!isNaN(userId)){
                fetch(this.$ENDPOINT+"/profile/" + userId)
                    .then(response => response.json())
                    .then(data => {
                        console.log("selected data:")
                        this.profileData = data.message;
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
            this.imageToUpdate = pic_;
            this.$refs.updatePics.style.display = show_ == true ? "flex" : "none";
            this.$refs.updateWhat.textContent = pic_ == "cover" ? "Update cover image" : "Update profile picture";
            if(show_ == false){
                this.imageToUpdate = "";
                this,this.imageFileToUpdate = "";
                this.$refs.updatePicUpload.className = "SECONDARY-BUTTON";
            }
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
                            });
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
        }

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

.profile-pic, .profile-pic > div{
    position: absolute;
    width: 20vh;
    height: 20vh;
    border-radius: 100vw;
    background-size: cover;
    background-position: center;
    background-image: url('../assets/images/default-user.jpg');
    border: 5px solid rgb(32, 33, 36);
    display: flex;
    align-items: flex-end;
    justify-content: center;
}

.profile-pic > div{
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

.profile-arroba{
    color: lightgray;
    margin-bottom: 1ch;
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

.update-pics{
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

.update-pics p{
    margin-bottom: 3ch;
}

.update-pics > div{
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

.update-pics > div > button{
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

}
</style>