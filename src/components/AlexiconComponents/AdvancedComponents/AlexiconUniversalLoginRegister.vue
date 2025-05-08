<template>
    <main class="AlexiconUniversalLoginRegister-MAIN" :style="bgImg ? `background-image: url('${bgImg}')`: ''">

        <section>
            <h1 v-if="mode == 'register'">Create an Alexicon Account to access <span :style="txtColor ? `color: ${txtColor} !important;`: ''">{{ serviceName }}</span></h1>
            <h1 v-if="mode == 'login'">Login into {{ serviceName }} with your Alexicon Account</h1>

            <div>
                <div v-if="step == 0">
                    <div><input type="text" placeholder="Email" v-model="email"></div>
                    <div><input type="password" placeholder="Password" v-model="password"></div>
                </div>
                <div v-if="mode == 'register' && step == 1">
                    <div><input type="text" placeholder="First name" v-model="firstName"></div>
                    <div><input type="text" placeholder="Last name" v-model="lastName"></div>
                    <div><input type="text" placeholder="Nickname" v-model="nickName"></div>
                    <div><input :type="inputType" placeholder="Birthday" @focus="inputType = 'date'" @blur="inputType = 'text'" v-model="birthday"></div>
                    <div class="AlexiconUniversalLoginRegister-genders">
                        <label @click.stop="manageGenderInput('male')">&nbsp;Male<AlexiconRadio style="pointer-events:none;" :styles="styles" :checked="genderInput.male" :key="genderInput.key"/></label>
                        <label @click.stop="manageGenderInput('female')">&nbsp;Female<AlexiconRadio style="pointer-events:none;" :styles="styles" :checked="genderInput.female" :key="genderInput.key"/></label>
                        <label @click.stop="manageGenderInput('other')">&nbsp;Other:<AlexiconRadio style="pointer-events:none;" :styles="styles" :checked="genderInput.other" :key="genderInput.key"/></label>
                    </div>
                    <div><input type="text" v-if="genderInput.other" placeholder="Gender..." v-model="genderInput.val"></div>
                </div>

            </div>

            <div>
                <p v-if="mode == 'register'" @click="mode = 'login', step = 0">Already have an account? Login</p>
                <p v-if="mode == 'login'" @click="mode = 'register', step = 0">Don't have an account? Register</p>
                <div>
                    <button class="Alexicon-icon-btn" v-if="step == 1" @click="step = 0"><MoveLeft/></button>
                    <AlexiconButton :styles="modifiedBtnStyles" v-if="step == 0 && mode == 'register' && modifiedBtnStyles" @click="step = 1">Continue</AlexiconButton>
                    <AlexiconButton :styles="styles" v-if="step == 1 && mode == 'register'" @click="register()">Create account</AlexiconButton>
                    <AlexiconButton :styles="styles" v-if="mode == 'login'" @click="login()">Login</AlexiconButton>
                </div>
            </div>
        </section>

    </main>
</template>

<script>
import { MoveLeft } from 'lucide-vue-next';
import AlexiconButton from '../BasicComponents/AlexiconButton.vue';
import AlexiconRadio from '../BasicComponents/AlexiconRadio.vue';

export default {
    name: 'UniversalLoginRegister',
    components: {
        AlexiconRadio,
        AlexiconButton,
        MoveLeft,
    },
    props: {
        styles: Object,
        bg: String,
        serviceName: String,
        apiBaseNameUrl: String,
        txtColor: String,
        bgImg: String,
    },
    data(){
        return{
            mode: 'register', // 'login' | 'register'
            step: 0,
            inputType: 'text',
            modifiedBtnStyles: false,
            email: '',
            password: '',
            firstName: '',
            lastName: '',
            nickName: '',
            birthday: '',
            genderInput: {
                male: false,
                female: false,
                other: false,
                key: 0,
                val: '',
            },
        }
    },
    methods: {

        manageGenderInput(option_){
            this.genderInput = {
                ...this.genderInput,
                male: false,
                female: false,
                other: false,
            };
            this.genderInput[option_] = true;
            this.genderInput.val = option_ == 'other' ? '' : option_;
            this.genderInput.key++;
        },

        login(){
            const access = {
                access_word: this.email,
                password: this.password,
            }

            fetch(this.$ENDPOINT+"/alexicon/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(access)
            })
            .then( data => data.json() )
            .then( data => {
                console.log(data)
                if(data.response == "Correct login."){
                    localStorage.setItem("AlexiconUserData", JSON.stringify({
                        sessionActive: true,
                        userData: data.user_data,
                        token: data.access_token
                    }));
                    this.$emit('activate-session', true);
                }
            })
        },

        register(){
            const userData = {
                email: this.email,
                password: this.password,
                name: this.firstName,
                surname: this.lastName,
                nickname: this.nickName,
                birthday: this.birthday,
                gender: this.genderInput.val
            };

            fetch(this.$ENDPOINT+"/alexicon/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userData)
            })
            .then( data => {
                console.log(data);
                if(data.response == "User added successfully."){
                    this.login();
                }
            })
        }

    },
    mounted(){
        this.modifiedBtnStyles = structuredClone(this.styles);
        this.modifiedBtnStyles.light.button.default.bg = "black";
        this.modifiedBtnStyles.dark.button.default.bg = "white";
        this.modifiedBtnStyles.dark.button.default.txt = "black";

        const alexiconUserData = JSON.parse(localStorage.getItem("AlexiconUserData"));
        if(alexiconUserData){
            this.$emit('activate-session', true);
        }
    }
}
</script>

<style scoped>
.AlexiconUniversalLoginRegister-MAIN{
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-position: center;
    background-size: cover;
}

.AlexiconUniversalLoginRegister-MAIN > section{
    width: fit-content;
    height: fit-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    max-width: 90vw;
    max-height: 90vh;
    background-color: light-dark(v-bind('styles.light.LoginRegister.bg'), v-bind('styles.dark.LoginRegister.bg'));
    padding: 2ch 3ch;
    border-radius: 10px;
}

.AlexiconUniversalLoginRegister-MAIN > section h1{
    margin: 0;
    margin-bottom: 1.5ch;
}

.AlexiconUniversalLoginRegister-MAIN input{
    margin-bottom: 0.75ch;
    width: 30ch;
    min-width: 30ch;
}

.AlexiconUniversalLoginRegister-MAIN section > div:nth-child(2) > div{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.AlexiconUniversalLoginRegister-genders{
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 25ch;
    margin-top: 0.5ch;
    margin-bottom: 0.5ch;
}

.AlexiconUniversalLoginRegister-genders label{
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    font-size: 1.25ch;
}

.AlexiconUniversalLoginRegister-MAIN > section > div:nth-child(3){
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    margin-top: 1.5ch;
}

.AlexiconUniversalLoginRegister-MAIN > section > div:nth-child(3) p{
    margin: 0;
    font-size: 1.5ch;
    font-style: italic;
    cursor: pointer;
}

.AlexiconUniversalLoginRegister-MAIN > section > div:nth-child(3) div{
    display: flex;
    align-items: center;
}

.AlexiconUniversalLoginRegister-MAIN > section > div:nth-child(3) .Alexicon-icon-btn{
    margin-top: 0.5ch;
    margin-right: 1ch;
    cursor: pointer;
}
</style>