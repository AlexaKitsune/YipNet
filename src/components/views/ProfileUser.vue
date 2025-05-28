<template>
    <main class="ProfileUser-MAIN">

        <div class="ProfileUser-cover">
            <img :src="userData?.current_cover_pic == '' || typeof userData?.current_cover_pic == 'object' ? require('../../assets/cover.png') : `${$ENDPOINT}/storage/${userData.current_cover_pic}`" data-aos="zoom-out">
            <div class="ProfileUser-edit" v-if="AlexiconUserData?.userData?.id == profileId" @click="showEditImages('cover')"><SquarePen/></div>
            <div class="ProfileUser-pfp" data-aos="zoom-in">
                <img :src="userData?.current_profile_pic == '' || typeof userData?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${userData.current_profile_pic}`">
                <div class="ProfileUser-edit" v-if="AlexiconUserData?.userData?.id == profileId" @click="showEditImages('pfp')"><SquarePen/></div>
            </div>
        </div>

        <!-- user info -->
        <div class="ProfileUser-info">
            <div data-aos="fade-right">
                <h1>{{ userData.name }} {{ userData.surname }}</h1>
                <div v-if="!editModes.active || editModes.type != 'description'">
                    <p v-if="userData?.description?.trim() != ''" ref="ProfileUser-description">{{ userData.description }}</p>
                    <p v-else><i class="ProfileUser-no-description" v-if="AlexiconUserData?.userData?.id == profileId">Add description</i></p>
                    <div class="ProfileUser-edit" v-if="AlexiconUserData?.userData?.id == profileId" @click="editModes = { active: true, type: 'description', modified: false}"><SquarePen/></div>
                </div>
                <div v-if="editModes.active && editModes.type == 'description'" class="ProfileUser-info-edit-desciption">
                    <AlexiconComponent :type="'textarea'" @get-val="(val) => { editModes.value = val, editModes.modified = true }" :resize="true" :standalone="true" :maxlength="128" :placeholder="'Edit description...'" :val="userData.description"/>
                    <div>
                        <button class="highlighted-btn" @click="updateDescription()">Save</button>
                        <button @click="editModes = { active: false, type: '', modified: false }">Cancel</button>
                    </div>
                </div>
            </div>

            <div class="ProfileUser-follow" data-aos="fade-left">
                <a :href="getFrontURL()+'/chat/'+userData.id"><button><MessageCircleMore/></button></a>
                <div v-if="AlexiconUserData?.userData?.id != profileId">
                    <button class="highlighted-btn" v-if="parseAndCheckIncludes(AlexiconUserData?.userData?.list_positive, profileId) === false" @click="manageFollow('follow')"><UserPlus style="margin-bottom:-4px;"/></button>
                    <button v-if="parseAndCheckIncludes(AlexiconUserData?.userData?.list_positive, profileId) === true" @click="manageFollow('unfollow')"><UserMinus style="margin-bottom:-4px;"/></button>
                    <button @click="manageBlock('block')" v-if="parseAndCheckIncludes(AlexiconUserData?.userData?.list_negative, profileId) === false"><Trash2 style="margin-bottom:-4px;"/></button>
                    <button @click="manageBlock('unblock')" v-else>Unblock</button>
                </div>
                <div>
                    <p><b>{{ userData?.list_positive_external?.length || 0 }}</b>&nbsp;Followers</p>
                    <p><b>{{ userData?.list_positive?.length || 0 }}</b>&nbsp;Following</p>
                </div>
            </div>
        </div>

        <!-- popup: update-pics -->
        <section class="update-pics" v-if="editModes.active && ['cover', 'pfp'].includes(editModes.type)">
            <div>
                <div class="ProfileUser-edit" @click="editModes = { active: false, type: ''}"><X/></div>
                <p>Update {{ editModes.type }}</p>
                <div class="update-pics-area" :class="`ProfileUser-img-prev-${editModes.type}`">
                    <img :src="editModes.value">
                    <input type="file" @change="setImagePreview()" ref="update-pics-input" accept="image/*">
                </div>
                <div>
                    <button class="highlighted-btn" :disabled="!editModes.modified" @click="uploadImage()">Save</button>
                    <button @click="editModes = { active: false, type: ''}">Cancel</button>
                </div>
            </div>
        </section>

        <br>
        
        <!-- post list -->
        <section v-for="(item, index) in postList" :key="index" style="overflow: hidden;">
            <PostRenderer :postData="item" :shared="false"/>
        </section>

    </main>
</template>

<script>
import { SquarePen, X, MessageCircleMore, UserPlus, UserMinus, Trash2 } from 'lucide-vue-next';
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';
import PostRenderer from '../comp/PostRenderer.vue';
import AOS from 'aos'
import 'aos/dist/aos.css'

export default {
    name: 'ProfileUser',
    components: {
        SquarePen, X, MessageCircleMore, UserPlus, UserMinus, Trash2, AlexiconComponent, PostRenderer,
    },
    data(){
        return{
            profileId: 0,
            userData: {},
            AlexiconUserData: {},
            editModes: {
                active: false,
                type: '', // "description" | "cover" | "pfp"
                value: undefined,
                modified: false,
            },
            postList: []
        }
    },
    methods: {
        getProfileId(){
			const path = new URL(window.location.href).pathname;
			let pathArray = path.split("/");
			// eslint-disable-next-line
			let x = pathArray.shift();
			this.profileId = pathArray[1];
        },

        getFrontURL(){
			return window.location.origin;
		},

        getPublicUserData(){
            fetch(`${this.$ENDPOINT}/alexicon/retrieve/?id=${this.profileId}`, {
                method: 'GET'
            })
            .then(res => res.json())
            .then(data => {
                this.userData = data;
                this.userData.list_positive = JSON.parse(data.list_positive);
                this.userData.list_positive_external = JSON.parse(data.list_positive_external);
                this.userData.list_negative = JSON.parse(data.list_negative);
                this.userData.list_negative_external = JSON.parse(data.list_negative_external);
                console.log("userData", this.userData)
            })
        },

        showEditImages(type_){
            let src;
            if(type_ == "cover") src = this.$ENDPOINT + "/storage/" +this.userData.current_cover_pic;
            if(type_ == "pfp") src = this.$ENDPOINT + "/storage/" +this.userData.current_profile_pic;
            this.editModes.active = true;
            this.editModes.type = type_;
            this.editModes.value = src;
        },

        setImagePreview() {
            const input = this.$refs["update-pics-input"];
            if (input && input.files && input.files[0]) {
                const file = input.files[0];
                const previewURL = URL.createObjectURL(file);
                this.editModes.value = previewURL;
                this.editModes.modified = true;
            }
        },

        uploadImage(){
            const input = this.$refs["update-pics-input"];
            const file = input.files[0];
            const targetPath = "yipnet/" + this.AlexiconUserData.userData.id;
            const token = this.AlexiconUserData.token;

            const formData = new FormData();
            formData.append('file', file);
            formData.append('targetPath', targetPath);

            fetch(this.$ENDPOINT+"/alexicon/upload", {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                console.log("uploadImage", data)
                console.log("Archivo subido:", data);
                if(data.status == "ok"){
                    this.updateImageInDatabase(data.relativePath);
                }
            })
            .catch(err => {
                console.error("Error al subir archivo:", err);
            });
        },

        updateImageInDatabase(imageUrl){
            const type = this.editModes.type;
            let picType;
            if(type == "cover") picType = "cover";
            if(type == "pfp") picType = "profile";
            const token = this.AlexiconUserData.token;

            fetch(this.$ENDPOINT + "/alexicon/update_pics", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    pic: picType,  // "profile" o "cover"
                    url: imageUrl
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "ok") {
                    this.editModes = {
                        active: false,
                        type: '',
                        value: '',
                        modified: false,
                    };
                    this.AlexiconUserData.userData[`current_${picType}_pic`] = imageUrl;
                    localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                    if(this.AlexiconUserData?.userData?.id == this.profileId){
                        this.userData[`current_${picType}_pic`] = imageUrl;
                    }
                }
            })
            .catch(err => {
                console.error("Error en la petición:", err);
            });
        },

        parseAndCheckIncludes(str, toSearch){
            let arr = [];
            try {
                arr = JSON.parse(str);
            } catch (error) {
                return 'error';
            }
            return arr.includes(parseInt(toSearch));
        },

        updateDescription(){
            const token = this.AlexiconUserData.token;
            const myUserData = this.AlexiconUserData.userData;

            const profileData = {
                name: myUserData.name,
                surname: myUserData.surname,
                nickname: myUserData.nickname,
                at_sign: myUserData.at_sign,
                gender: myUserData.gender,
                description: this.editModes.value,
            };

            fetch(this.$ENDPOINT + '/alexicon/update_profile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(profileData),
            })
            .then(res => res.json())
            .then(data => {
                console.log(data)
                const desc = this.editModes.value;
                if(data.status == "ok"){
                    this.AlexiconUserData.userData.description = desc;
                    localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                }
                this.editModes.active = false;
                this.editModes.value = '';
                this.editModes.modified = false;
                this.$nextTick(() => {
                    setTimeout(() => {
                        this.$refs["ProfileUser-description"].textContent = desc;
                    }, 100);
                });
            })
            .catch(err => {
                console.error("Error en la petición:", err);
                this.editModes.active = false;
                this.editModes.value = '';
                this.editModes.modified = false;
            });
        },

        manageFollow(mode){
            const token = this.AlexiconUserData.token;
            const targetId = parseInt(this.profileId);

            fetch(`${this.$ENDPOINT}/alexicon/follow`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ targetId, mode })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "ok") {
                        let myListPositive = JSON.parse(this.AlexiconUserData.userData.list_positive);
                        let targetListPositive = this.userData.list_positive_external;
                        if(mode == "follow"){
                            if (!myListPositive.includes(targetId)) {
                                myListPositive.push(targetId);
                            }
                            if (!targetListPositive.includes(this.AlexiconUserData.userData.id)) {
                                targetListPositive.push(this.AlexiconUserData.userData.id);
                            }
                        }else
                        if(mode == "unfollow"){
                            myListPositive = myListPositive.filter(num => num !== targetId);   
                            targetListPositive = targetListPositive.filter(num => num !== this.AlexiconUserData.userData.id);
                        }
                        this.AlexiconUserData.userData.list_positive = JSON.stringify(myListPositive);
                        localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                        this.userData.list_positive_external = targetListPositive;
                    } else {
                        console.error("Error:", data.message);
                    }
                })
                .catch(err => {
                    console.error("Error with the request:", err);
                });
        },

        manageBlock(mode){
            const token = this.AlexiconUserData.token;
            const targetId = parseInt(this.profileId);

            fetch(`${this.$ENDPOINT}/alexicon/block`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ targetId, mode })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "ok") {
                        let myListNegative = JSON.parse(this.AlexiconUserData.userData.list_negative);
                        if(mode == "block"){
                            if (!myListNegative.includes(targetId)) {
                                myListNegative.push(targetId);
                            }
                            const path = new URL(window.location.href).pathname;
                            const newPath = window.location.href.replace(path, "/");
                            window.location.href = newPath;
                        }else
                        if(mode == "unblock"){
                            myListNegative = myListNegative.filter(num => num !== targetId);   
                        }
                        this.AlexiconUserData.userData.list_negative = JSON.stringify(myListNegative);
                        localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                    } else {
                        console.error("Error:", data.message);
                    }
                })
                .catch(err => {
                    console.error("Error with the request:", err);
                });
        },

        listPosts(){
            const token = this.AlexiconUserData.token;
            
            fetch(this.$ENDPOINT + `/yipnet/list_posts/${this.profileId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(res => res.json())
            .then(data => {
                console.log(data);
                if(data.status == "ok"){
                    this.postList = data.post_list;
                }
            });
        }

    },

    mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.getProfileId();

        const targetId = parseInt(this.profileId);
        const myListNegative = JSON.parse(JSON.parse(localStorage.getItem("AlexiconUserData")).userData.list_negative);
        if(myListNegative.includes(targetId)){
            const path = new URL(window.location.href).pathname;
            const newPath = window.location.href.replace(path, "/");
            window.location.href = newPath;
        }

        this.getPublicUserData();
        this.listPosts();

        AOS.init();
    }
}
</script>

<style scoped>
.ProfileUser-MAIN{
    display: flex;
    flex-direction: column;
    max-width: 1080px;
    margin: 0 auto;
}

.ProfileUser-cover{
    position: relative;
    width: 100%;
    aspect-ratio: 3/1 !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.ProfileUser-cover > *{
    position: absolute;
}

.ProfileUser-cover > img{
    width: 100%;
    height: 100%;
    display: flex;
    object-fit: cover;
    border-radius: 0 0 10px 10px;
}

.ProfileUser-pfp{
    border: 1ch solid black;
    height: 50%;
    aspect-ratio: 1/1;
    border-radius: 100vw;
    overflow: hidden;
}

.ProfileUser-pfp > img{
    width: 100%;
    height: 100%;
    display: flex;
    object-fit: cover;
}

.ProfileUser-edit{
    border-radius: 5px;
    aspect-ratio: 1/1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 3ch;
}

.ProfileUser-edit:hover{
    cursor: pointer;
    scale: 1.1;
}

.ProfileUser-cover .ProfileUser-edit{
    z-index: 2;
    background-color: rgba(0, 0, 0, 0.75);
    box-shadow: 0 0 1ch rgba(0, 0, 0, 0.5);
    position: absolute;
}

.ProfileUser-cover > .ProfileUser-edit{
    bottom: 1ch;
    right: 1ch;
}

.ProfileUser-pfp > .ProfileUser-edit{
    bottom: 1ch;
    right: 0;
    left: 0;
    margin: 0 auto;
}

/* info */
.ProfileUser-info{
    display: flex;
    justify-content: flex-start;
}

.ProfileUser-info > div:first-child{
    width: 100%;
}

.ProfileUser-info > div:first-child > div{
    display: inline-flex;
    align-items: flex-start;
    width: 100%;
}

.ProfileUser-info > div:first-child > div p{
    margin: 0;
}

.ProfileUser-info > div:first-child > div .ProfileUser-edit{
    margin-left: 1ch;
}

.ProfileUser-info > div:first-child > div button{
    margin-left: 3ch;
}

.AlexiconTextarea-MAIN{
    width: 100% !important;
}

.ProfileUser-info-edit-desciption{
    display: flex;
    flex-direction: column;
}

.ProfileUser-info-edit-desciption > div:last-child{
    width: 100%;
    display: flex;
    justify-content: flex-end;
}

.ProfileUser-info > div:last-child{
    width: fit-content;
    margin-left: calc(1ch + 1vw);
    display: flex;
    flex-direction: row;
    height: fit-content;
    margin-top: 2ch;
}

.ProfileUser-info > div:last-child > div{
    display: flex;
    flex-direction: row;
    align-items: center;
}

.ProfileUser-info > div:last-child > div p, .ProfileUser-info > div:last-child > div button, .ProfileUser-follow > button{
    margin-left: 2ch;
}

.ProfileUser-info > div:last-child > div p{
    display: flex;
}

.ProfileUser-no-description{
    opacity: 0.5;
}

.ProfileUser-follow{
    display: flex;
    align-items: center;
}

.ProfileUser-follow button{
    min-width: 5ch !important;
}

.ProfileUser-follow button{
    height: 4ch !important;
}

/* update-pics */
.update-pics{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 2;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.update-pics > div{
    position: relative;
    color: light-dark(black, white);
    background-color: light-dark(white, #222222);
    border-radius: 10px;
    padding: 1ch;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: calc(95vw - 2ch);
}

.update-pics > div > .ProfileUser-edit{
    position: absolute;
    top: 1ch;
    right: 1ch;
}

.update-pics > div > p{
    width: 100%;
}

.ProfileUser-img-prev-cover, .ProfileUser-img-prev-pfp{
    margin: 3ch 0;
    scale: 0.95;
    position: relative;
    background-color: rgba(128, 128, 128, 0.25);
    overflow: hidden;
}

.ProfileUser-img-prev-cover:hover, .ProfileUser-img-prev-pfp:hover{
    scale: 1;
}

.ProfileUser-img-prev-cover > img, .ProfileUser-img-prev-pfp > img{
    display: flex;
    width: 100%;
    height: 100%;
    object-position: center;
    background-size: cover;
    pointer-events: none;
    object-fit: cover;
}

.ProfileUser-img-prev-cover > input, .ProfileUser-img-prev-pfp > input{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    cursor: crosshair;
    opacity: 0;
}

.ProfileUser-img-prev-cover{
    width: 40ch;
    aspect-ratio: 3/1 !important;
    max-width: 80vw;
    border-radius: 5px;
}

.ProfileUser-img-prev-pfp{
    width: 25ch;
    aspect-ratio: 1/1 !important;
    border-radius: 100vw;
}

.update-pics > div > div:last-child{
    width: 100%;
    display: flex;
    justify-content: flex-end;
    margin-top: 1ch;
}

.update-pics > div > div:last-child button{
    margin-left: 3ch;
}
</style>