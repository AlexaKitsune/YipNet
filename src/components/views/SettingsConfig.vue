<template>
    <main class="SettingsConfing-MAIN">
        <h1>Settings</h1>

        <!-- basic -->
        <section class="SettingsConfig-basic">
            <h1>Profile settings</h1>
            <div>
                <p>Name</p>
                <AlexiconComponent :type="'text'" :val="basic.name" @get-val="(val) => {basic.name = val, basic.modified = true}"/>
            </div>
            <div>
                <p>Last name</p>
                <AlexiconComponent :type="'text'" :val="basic.surname" @get-val="(val) => {basic.surname = val, basic.modified = true}"/>
            </div>
            <div>
                <p>Nickname</p>
                <AlexiconComponent :type="'text'" :val="basic.nickname" @get-val="(val) => {basic.nickname = val, basic.modified = true}"/>
            </div>
            <div>
                <p>@</p>
                <AlexiconComponent :type="'text'" :val="basic.at_sign" @get-val="(val) => {basic.at_sign = val, basic.modified = true}"/>
            </div>
            <div>
                <p>Gender</p>
                <div class="SettingsConfig-genders">
                    <label @click.stop="basic.gender = 'male'">&nbsp;Male<div style="pointer-events:none !important;"><AlexiconComponent :type="'radio'" :checked="basic.gender == 'male'" :key="`male-${basic.gender}`"/></div></label>
                    <label @click.stop="basic.gender = 'female'">&nbsp;Female<div style="pointer-events:none !important;"><AlexiconComponent :type="'radio'" :checked="basic.gender == 'female'" :key="`female-${basic.gender}`"/></div></label>
                    <label @click.stop="basic.gender = ''">&nbsp;Other<div style="pointer-events:none !important;"><AlexiconComponent :type="'radio'" :checked="basic.gender != 'male' && basic.gender != 'female'" :key="`other-${basic.gender}`"/></div></label>
                </div>
                <AlexiconComponent v-if="basic.gender != 'male' && basic.gender != 'female'" :type="'text'" :val="basic.gender" @get-val="(val) => {basic.gender = val, basic.modified = true}" :placeholder="'Preferred gender'"/>
            </div>

            <button class="highlighted-btn" v-if="basic.modified" @click="updateBasicProfile()">Save</button> <br v-else>
        </section>

        <!-- block -->
        <section class="SettingsConfig-block">
            <h1>Blocked users</h1>
            <div v-if="blockedUsers.length == 0"><p style="opacity:0.5;">There are not blocked users.</p></div>
            <div v-for="(item, index) in blockedUsers" :key="index" class="SettingsConfig-blocked-user">
                <div>
                    <img :src="item?.current_profile_pic == '' || typeof item?.current_profile_pic == 'object' ? require('../../assets/pfp.png') : `${$ENDPOINT}/storage/${item?.current_profile_pic}`">
                    <p>{{ item.name }} {{ item.surname }}</p>
                </div>
                <button class="highlighted-btn" @click="unblock(item.id)">Unblock</button>
            </div>
        </section>

        <!-- pass -->
        <section class="SettingsConfig-pass">
            <h1>Change password</h1>
            <div><p style="opacity:0.5;">Remember that this will not only change your password <br>for YipNet, but for the entire Alexicon ecosystem.</p></div>
            <div>
                <p>Old password</p>
                <AlexiconComponent :type="'password'" :val="password.valOldPass" @get-val="(val) => {password.valOldPass = val, password.modified = true}"/>
            </div>
            <div>
                <p>New password</p>
                <AlexiconComponent :type="'password'" :val="password.valNewPass" @get-val="(val) => {password.valNewPass = val, password.modified = true}"/>
            </div>
            <div>
                <p>Confirm new password</p>
                <AlexiconComponent :type="'password'" :val="password.valConfirmNewPass" @get-val="(val) => {password.valConfirmNewPass = val, password.modified = true}"/>
            </div>
            <button class="highlighted-btn" v-if="password.modified" @click="changePass()">Update password</button> <br v-else>
        </section>

    </main>
</template>

<script>
import AlexiconComponent from '../AlexiconComponents/AlexiconComponent.vue';

export default {
    name: 'SettingsConfig',
    components: {
        AlexiconComponent
    },
    data(){
        return{
            AlexiconUserData: {},
            basic: {
                name: '',
                surname: '',
                nickname: '',
                at_sign: '',
                gender: '',
                modified: false,
            },
            blockedUsers: [],
            password: {
                valOldPass: '',
                valNewPass: '',
                valConfirmNewPass: '',
                modified: false,
            },
        }
    },
    methods: {
        async updateBasicProfile(){
            const b = this.basic;
            const profileData = {
                name: b.name,
                surname: b.surname,
                nickname: b.nickname,
                at_sign: b.at_sign,
                gender: b.gender,
                description: this.AlexiconUserData.userData.description,
            };

            if(profileData.name.trim() == '' || profileData.surname.trim() == '' || profileData.nickname.trim() == '' || profileData.gender.trim() == ''){
                return;
            }

            const result = await this.alexicon_UPDATE_PROFILE(this.$ENDPOINT, this.TOKEN(), profileData);
            if(result.status == "ok"){
                this.AlexiconUserData.userData.name = profileData.name;
                this.AlexiconUserData.userData.surname = profileData.surname;
                this.AlexiconUserData.userData.nickname = profileData.nickname;
                this.AlexiconUserData.userData.at_sign = profileData.at_sign;
                this.AlexiconUserData.userData.gender = profileData.gender;
                localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                this.basic.modified = false;
            }
        },

        async unblock(id_){
            const result = await this.alexicon_BLOCK(this.$ENDPOINT, this.TOKEN(), { targetId: id_, mode: "unblock" });
            if(result.status == "ok"){
                let list_negative = JSON.parse(this.AlexiconUserData.userData.list_negative);
                list_negative = list_negative.filter(item => item !== id_);
                this.AlexiconUserData.userData.list_negative = JSON.stringify(list_negative);
                localStorage.setItem("AlexiconUserData", JSON.stringify(this.AlexiconUserData));
                const arr = JSON.parse(this.AlexiconUserData.userData.list_negative);
                this.blockedUsers = await this.alexicon_RETRIEVE_USERS(this.$ENDPOINT, { ids: arr });
            }
        },

        async changePass(){
            const oldPass = this.password.valOldPass;
            const newPass = this.password.valConfirmNewPass;
            const confirmPass = this.password.valNewPass;

            if(newPass != confirmPass){
                console.log("Passwords dont match");
                return;
            }

            const result = await this.alexicon_UPDATE_PASS(this.$ENDPOINT, this.TOKEN(), { oldPass, newPass });
            if(result.status == "ok"){
                console.log("Contraseña actualizada con éxito.");
                this.password = {
                    valOldPass: '',
                    valNewPass: '',
                    valConfirmNewPass: '',
                    modified: false,
                }
            }
        }
    },
    async mounted(){
        this.AlexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        this.basic = {
            name: this.AlexiconUserData.userData.name,
            surname: this.AlexiconUserData.userData.surname,
            nickname: this.AlexiconUserData.userData.nickname,
            at_sign: this.AlexiconUserData.userData.at_sign,
            gender: this.AlexiconUserData.userData.gender,
        }
        this.$nextTick(() => {
            this.basic.modified = false;
            this.password.modified = false;
        });

        const arr = JSON.parse(this.AlexiconUserData.userData.list_negative);
        this.blockedUsers = await this.alexicon_RETRIEVE_USERS(this.$ENDPOINT, { ids: arr });
    }
}
</script>

<style scoped>
.SettingsConfing-MAIN{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.SettingsConfing-MAIN > section{
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
    background-color: #2d2d2d;
    background-color: light-dark(#f2f2f2, #2d2d2d);
    position: relative;
    display: flex;
    flex-direction: column;
    width: 75ch;
    max-width: calc(100vw - 6ch);
}

h1{
    max-width: 75vw;
}

.SettingsConfing-MAIN > section div{
    width: 50%;
    min-width: fit-content;
    margin: 0 auto;
    margin-bottom: 10px;
}

.SettingsConfing-MAIN > section div p{
    margin-top: 5px;
    margin-bottom: 5px;
}

.SettingsConfing-MAIN > section div:deep(input){
    width: 100%;
}

.SettingsConfing-MAIN > section button{
    margin-left: auto !important;
    position: relative;
}

.SettingsConfig-blocked-user{
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.SettingsConfig-blocked-user > div{
    margin: 0 !important;
    margin-left: 0 !important;
    display: flex;
    align-items: center;
    width: fit-content !important;
}

.SettingsConfig-blocked-user > div img{
    width: 40px;
    aspect-ratio: 1/1;
    object-fit: cover;
    object-position: center;
    border-radius: 100vw;
    margin-right: 10px;
}

/* gender */
.SettingsConfig-genders{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100% !important;
}

label{
    display: flex;
    flex-direction: row-reverse;
    cursor: pointer;
    margin-top: 10px;
}
</style>