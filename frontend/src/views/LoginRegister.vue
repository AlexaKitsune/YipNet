<template>
    <main>

        <h1></h1>
        <h2>{{ mode.charAt(0).toUpperCase() + mode.slice(1) }}</h2>
        <p :style="`color: ${serverMsg.color};`">{{ serverMsg.content }}</p>

        <section>
            <div><input type="email" placeholder="Email" ref="accessEmail" v-model="accessData.email"></div>
            <div><input type="password" placeholder="Password" ref="accessPassword" v-model="accessData.password"></div>
        </section>

        <section v-if="mode === 'login'">
            <button class="BIG-BUTTON MAIN-BUTTON" @click="login()">Login</button>
            <button class="MIN-BUTTON" @click="switchMode('register')">Register</button>
        </section>

        <section v-if="mode === 'register'">
            <div><input type="text" placeholder="First name" ref="accessFirstName" v-model="accessData.firstName"></div>
            <div><input type="text" placeholder="Last name" ref="accessLastName" v-model="accessData.lastName"></div>
            <div><input type="date" ref="accessDate" v-model="accessData.birthday"></div>
            <div class="gender-radio-set">
                <label><input type="radio" name="gender" value="male" v-model="accessData.gender">Male</label>
                <label><input type="radio" name="gender" value="female" v-model="accessData.gender">Female</label>
                <label><input type="radio" name="gender" :value="this.$refs.otherGender?.value || 0" v-model="accessData.gender">Other</label>
            </div>
            <div v-if="accessData.gender != 'male' && accessData.gender != 'female' && accessData.gender != undefined"><input type="text" ref="otherGender" placeholder="Custom gender"></div>
            <button class="BIG-BUTTON MAIN-BUTTON" @click="register()">Register</button>
            <button class="MIN-BUTTON" @click="switchMode('login')">Login</button>
        </section>

    </main>
</template>

<script>
export default {
    name: 'LoginRegister',
    data(){
        return{
            mode: "login",
            accessData: {
                email: undefined,
                password: undefined,
                firstName: undefined,
                lastName: undefined,
                birthday: undefined,
                gender: undefined
            },
            serverMsg: {
                color: "transparent",
                content: ""
            }
        }
    },

    methods:{

        switchMode(switchTo_){
            this.mode = switchTo_;
        },

        login(){
            console.log(this.accessData);
            fetch(this.$ENDPOINT+"/login", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.accessData.email,
                        password: this.accessData.password
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Respuesta del servidor:', data);
                    if(data.status == "ok")
                        this.accessSession(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(error)
                });
        },

        register(){
            console.log(this.accessData);
            fetch(this.$ENDPOINT+"/register", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        name: this.accessData.firstName,
                        surname: this.accessData.lastName,
                        birthday: this.accessData.birthday,
                        gender: this.accessData.gender,
                        email: this.accessData.email,
                        password: this.accessData.password
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Respuesta del servidor:', data);
                    if(data.message.response){
                        console.log("Cuenta creada")
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        },

        accessSession(data_){
            const yipUserData = {
                "sessionStatus": true,
                "token": data_.message.access_token,
                "userData": data_.message.user_data
            }
            localStorage.setItem("yipUserData", JSON.stringify(yipUserData));
            window.location.hash = "/newsfeed";
            window.location.reload();
        }

    }
}
</script>

<style scoped>
main{
    display: flex;
    flex-direction: column;
    align-items: center;
}

main h1, main h2{
    color: white;
    font-family: sans-serif;
}

main > section{
    display: inherit;
    flex-direction: inherit;
    align-items: inherit;
    width: calc(100% - 2ch);
    max-width: 256px;
}

main > section > *{
    margin: 1ch;
    width: 100%;
    display: inherit;
    flex-direction: inherit;
    align-items: inherit;
}

input{
    width: calc(100% - 2ch);
}

.gender-radio-set{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.gender-radio-set > label {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    color: white;
    font-family: sans-serif;
}
</style>