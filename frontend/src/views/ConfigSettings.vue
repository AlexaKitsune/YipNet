<template>
    <main>
        <h1>Settings ⚙️⚙️⚙️</h1>

        <button class="MAIN-BUTTON logout" @click="logOut()">Log out</button>

        <!--{{ userData }}-->

        <section class="settings-general">
            <h2>General settings</h2>
            <div class="settings-names">
                <div>First name: <input type="text" required v-model="profileGeneralSettings.name"></div>
                <div>Last name: <input type="text" required v-model="profileGeneralSettings.surname"></div>
            </div>
            <div class="set-description">Description:
                <textarea v-model="profileGeneralSettings.description"></textarea>
            </div>
            <div>Birthday:
                <input type="date" :v-model="profileGeneralSettings.birthday" required>
            </div>
            <div class="set-gender">Gender:
                <div>
                    <label>
                        <input type="radio" name="gender" value="male" v-model="profileGeneralSettings.gender">Male
                    </label>
                    <label>
                        <input type="radio" name="gender" value="female" v-model="profileGeneralSettings.gender">Female
                    </label>
                    <label>
                        <input type="radio" name="gender" value="other" v-model="profileGeneralSettings.gender" ref="otherGenderInput">Other
                    </label>
                </div>
                <div v-if="profileGeneralSettings.gender != 'male' && profileGeneralSettings.gender != 'female'">
                    <input type="text" name="customGender" ref="otherGender" placeholder="Custom gender" v-model="customGender">
                </div>
            </div>
            <div>Blocked users:
                {{ userData.postList }}
            </div>

            <button class="BIG-BUTTON MAIN-BUTTON" @click="updateProfile()">Update profile</button>
        </section>

        <!--{{ profileGeneralSettings }}-->
        <!--{{ customGender }}-->

        <hr v-if="allowAPI">

        <section class="settings-api" v-if="allowAPI">
            <h2>API code</h2>
            <div v-if="userData.apiCode == 0" class="set-api-not-exists">
                <h3>You don't have an API code yet!</h3>
                <br><br>
                <span>With your API code, you can:</span>
                <ul>
                    <li>Post content</li>
                    <li>Delete your own posts</li>
                    <li>Retrieve information from any user profile with public information</li>
                    <!--<li>View a list of your notifications</li>-->
                    <!--<li>Send and receive messages</li>-->
                </ul>
                <div><button class="MAIN-BUTTON" @click="apiKeyActions('generate')">Generate your API Code</button></div>
            </div>
            <div v-else class="set-api-exists">
                <h3>API key generated</h3>
                <p>
                    Your API key has been generated. Please keep it safe and do not share it with others. 
                    It's important to keep your API key confidential to ensure the security of your account.
                    You can use this key to access certain features of our service. If you lose your API key, 
                    you can request a new one in your account settings.
                </p>
                <div v-if="apiCodeKey == ''"><button class="MAIN-BUTTON" @click="apiKeyActions('get')">See your API key</button></div>
                <div v-else><input type="text" disabled :value="apiCodeKey" ref="apiCodeKeyInput"><button class="MAIN-BUTTON copy-btn" @click="copyToClipboard">Copy</button></div>

                <br>
            
                <span>With your API code, you can:</span>
                <ul>
                    <li>Post content</li>
                    <li>Delete your own posts</li>
                    <li>Retrieve information from any user profile with public information</li>
                    <!--<li>View a list of your notifications</li>-->
                    <!--<li>Send and receive messages</li>-->
                </ul>
                <h3>How to use my API key?</h3>
                <p>
                    To use your API key, you can make HTTP requests to our server with the API key included in the request headers. Below are examples in JavaScript and Python on how to use your API key:
                </p>

                <br>

                <div>
                    <button @click="setCodeExample('js')" :class="`BIG-BUTTON SECONDARY-BUTTON ${exampleCode == 'js'? 'selected-lang-button' : ''}`">Javascript</button>
                    &nbsp;&nbsp;&nbsp;
                    <button @click="setCodeExample('py')" :class="`BIG-BUTTON SECONDARY-BUTTON ${exampleCode == 'py'? 'selected-lang-button' : ''}`">Python</button>
                </div>
                
                <div class="settings-example-code">
                    <ApiDocs :lang="exampleCode" :userId="userData.id"/>
                </div>
            </div>
        </section>

        <hr>

        <section class="settings-password">
            <h2>Change password</h2>
            <p>Current password:</p>
            <input type="password" required ref="inputOldPass">
            <p><br>New password:</p>
            <input type="password" required ref="inputNewPass1">
            <p>Confirm new password:</p>
            <input type="password" required ref="inputNewPass2">

            <p v-if="passwordError.active" class="error-pass">{{ passwordError.msg }}</p>
            <button class="BIG-BUTTON MAIN-BUTTON" @click="updatePass()" ref="updatePwBtn">Update password</button>
        </section>

        <div v-if="popUpOkUpdates.active" class="popUpOkUpdates">
            <div>
                <div class="popUpOkUpdatesClose" @click="popUpOkUpdates.active = false;">+</div>
                <p>{{ popUpOkUpdates.msg }}</p>
                <button @click="popUpOkUpdates.active = false;" class="BIG-BUTTON MAIN-BUTTON">Ok</button>
            </div>
        </div>

    </main>
</template>

<script>
import ApiDocs from '@/components/ApiDocs.vue';
export default {
  components: { ApiDocs },
    name: 'ConfigSettings',
    data(){
        const userData = JSON.parse(localStorage.getItem("yipUserData")).userData;
        const customGender = '';
        const profileGeneralSettings = {
            name: userData.name,
            surname: userData.surname,
            description: userData.description,
            birthday: userData.birthday,
            gender: userData.gender,
            negativeList: JSON.stringify(userData.negativeList == null ? [] : userData.negativeList),
        }
        return {
            userData,
            apiCodeKey: "",
            exampleCode: "",
            allowAPI: false, //Cambiar a true cuando acabe su desarrollo
            profileGeneralSettings,
            customGender,
            passwordError: {active: false, msg: ""},
            popUpOkUpdates: {active: false, msg: ""},
        };
    },

    methods:{

        apiKeyActions(action_){
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/api/" + action_, {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + token // Donde "token" es el token de autorización que deseas enviar
                }})
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if(data.status == "ok"){
                        if(action_ == "get"){
                            this.apiCodeKey = data.message.key;
                        }else{
                            let updatedUserData = JSON.parse(localStorage.getItem("yipUserData"));
                            updatedUserData.userData.apiCode = 1;
                            localStorage.setItem("yipUserData", JSON.stringify(updatedUserData));
                            this.userData.apiCode = 1;
                            console.log(data.message.key);
                            this.apiCodeKey = data.message.key;
                        }
                    }
                })
                .catch(error => {
                    console.error("Error: ", error);
                }); 
        },

        copyToClipboard() {
            this.$refs.apiCodeKeyInput.select();
            // Intenta copiar el contenido seleccionado al portapapeles
            try {
                document.execCommand('copy');
                console.log("Texto copiado");
            } catch (err) {
                console.log("Error al copiar");
            }
            // Deselecciona el input
            window.getSelection().removeAllRanges();
        },

        setCodeExample(lang_){
            this.exampleCode = lang_;
        },

        updateProfile(){
            let currentGender = this.profileGeneralSettings.gender;
            currentGender = currentGender == "other" ? this.customGender: currentGender;
            let profileGeneralSettingsCopy = this.profileGeneralSettings;
            profileGeneralSettingsCopy.gender = currentGender;

            if(profileGeneralSettingsCopy.description == undefined)
                profileGeneralSettingsCopy.description = "";

            if(currentGender != "male" && currentGender != "female")
                setTimeout(() => {
                    this.$refs.otherGenderInput.checked = true; 
                }, 80);
            
            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/update_profile", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: JSON.stringify(profileGeneralSettingsCopy)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if(data.status == "ok"){
                    let yipUserData = JSON.parse(localStorage.getItem('yipUserData'));
                    yipUserData.userData.description = profileGeneralSettingsCopy.description;
                    localStorage.setItem("yipUserData", JSON.stringify(yipUserData));
                    this.popUpOkUpdates.active = true;
                    this.popUpOkUpdates.msg = "Profile updated successfully";
                }
            })
        },

        updatePass(){
            const oldPass = this.$refs.inputOldPass;
            const newPass1 = this.$refs.inputNewPass1;
            const newPass2 = this.$refs.inputNewPass2;
            if(oldPass.value == ""){
                oldPass.focus();
                return;
            }
            if(newPass1.value == ""){
                newPass1.focus();
                return;
            }
            if(newPass2.value == ""){
                newPass2.focus();
                return;
            }
            if(newPass1.value != newPass2.value){
                this.passwordError.active = true;
                this.passwordError.msg = "Both new passwords do not match";
                return;
            }
            this.$refs.updatePwBtn.style.opacity = 0.5;
            this.$refs.updatePwBtn.style.pointerEvents = "none";
            this.passwordError.active = false;

            const token = JSON.parse(localStorage.getItem("yipUserData")).token;
            fetch(this.$ENDPOINT+"/update_pass", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Incluye el token JWT en el encabezado
                },
                body: JSON.stringify({
                    oldPass: oldPass.value,
                    newPass: newPass1.value,
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.$refs.updatePwBtn.style.opacity = 1;
                this.$refs.updatePwBtn.style.pointerEvents = "all";
                this.passwordError.active = true;
                if(data.message == "Incorrect old password"){
                    this.passwordError.message = "Incorrect current password.";
                }
                if(data.message == "New password does not meet the required criteria"){
                    this.passwordError = "Password must be at least 8 characters, at least 1 number, 1 uppercase, 1 lowercase and 1 special character";
                }
                if(data.status == "ok" || data.message == "Password updated successfully"){
                    this.passwordError.active = false;
                    this.popUpOkUpdates.active= true;
                    this.popUpOkUpdates.msg = "Password updated successfully";
                }
            })
        },

        logOut(){
            localStorage.clear();
            sessionStorage.clear();
            setTimeout(() => {
                window.location.reload();
            }, 80);
        }

    },
    
    beforeCreate(){
        if(JSON.parse(localStorage.getItem("yipUserData"))  == null)
            window.location.hash = "/access";
    }
}
</script>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    align-items: center;
}

main > section{
    width: 90%;
    display: flex;
    flex-direction: column;
}

main > .logout{
    align-self: flex-end;
    margin-right: 5vw;
    color: orange;
}

main > .logout:hover{
    background-color: orange;
    color: black;
}

main > section > button{
    margin-top: 5ch;
    margin-bottom: 5ch;
    width: fit-content;
    align-self: center;
}

main > hr{
    width: 90%;
}

main input, main textarea{
    margin-top: 1ch;
    padding: 1ch;
    border-radius: 1ch;
    border: 1px solid transparent;
    background-color: rgba(50, 50, 55, 1);
}

.settings-names{
    display: flex;
    
    justify-content: space-between;
}

.settings-names > div{
    display: flex;
    flex-direction: column;
    width: 48%;
    margin-bottom: 2ch;
}

.set-description{
    display: flex;
    flex-direction: column;
}

.set-description textarea{
    resize: vertical;
    margin-bottom: 2ch;
}

input[type=date]{
    margin-bottom: 2ch;
}

.set-gender{
    margin-bottom: 2ch;
}

.set-gender > div{
    width: 100%;
    margin-top: 1ch;
}

.set-gender > div > input{
    width: calc(100% - 2ch);
}

.set-api-not-exists > div, .set-api-exists > div{
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1ch;
}

.set-api-not-exists button, .set-api-exists button{
    padding: 0.5ch 1ch;
}

.set-api-exists input{
    width: 100%;
    color: wheat;
    font-family: monospace;
}

.set-api-exists > div *{
    margin: 0;
}

.set-api-exists .copy-btn{
    margin-left: 1ch;
    margin-top: 0;
}

.selected-lang-button{
    color: black;
    background-color: aqua;
}

.settings-password p{
    margin-bottom: 0.5ch;
}

.error-pass{
    color:orange;
}

.popUpOkUpdates{
    position: fixed;
    z-index: 10;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: rgba(0,0,0,0.5);
}

.popUpOkUpdates > div{
    background-color: #343538;
    padding: 2ch;
    border-radius: 2ch;
    box-shadow: 0ch 0ch 2ch rgba(0, 0, 0, 0.5);
    position: relative;
    min-width: 20ch;
    min-height: 10ch;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.popUpOkUpdates p{
    margin: 2ch;
    margin-top: 3ch;
}

.popUpOkUpdatesClose{
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
    top: 1ch;
    right: 1ch;
}

.popUpOkUpdatesClose:hover{
    cursor: pointer;
    color: lightgray;
    transition: all 0.2s;
}

/********************************************************************
* RESPONSIVE
********************************************************************/
@media all and (max-width:780px){

    main > section > button{
        width: 100%;
    }

    .settings-names{
        flex-direction: column;
    }

    .settings-names > div{
        margin-right: 0;
        margin-bottom: 1ch;
        width: 100%;
    }

}
</style>