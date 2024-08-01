<template>
    <main>
        <div>

            <div v-if="verificationStatus">
                <h1>Welcome to YipNet!</h1>
                <p>Your account has been activated successfully</p>
            </div>

            <div v-if="!verificationStatus && !errorStatus">
                <h1>Welcome to YipNet!</h1>
                <p>The requested account does not exist or has already been verified</p>
            </div>

            <div v-if="errorStatus">
                <h1>There was an error verifying the account</h1>
            </div>

            <br>
            <button class="BIG-BUTTON MAIN-BUTTON">Go back to Newsfeed</button>

        </div>
    </main>
</template>

<script>
export default {
    name: 'VerifyAccount',
    data(){
        return{
            verificationStatus: false,
            errorStatus: false,
        }
    },
    methods: {
        getNumbersAndVerify(){
            let text = window.location.href;
            text = text.split("verify")[1];
            let result = text.replace("~", "");
            const id = result.split("&")[0];
            const verifykey = result.split("&")[1];
            console.log(id, verifykey)

            fetch(this.$ENDPOINT + "/verify", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "receivedId": id,
                    "receivedVerifyKey": verifykey
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                if(data.status == "ok"){
                    if(data.message.response == "verified"){
                        this.verificationStatus = true;
                        let yipUserData = JSON.parse(localStorage.getItem('yipUserData'));
                        yipUserData.userData.verified = '1';
                        localStorage.setItem("yipUserData", JSON.stringify(yipUserData));
                        this.$parent.verifyAccData.verifiedAccount = 1;
                        this.$parent.verifyAccData.showVerifyAlert = false;
                    }else{
                       this.verificationStatus = false; 
                    }
                }else{
                    this.verificationStatus = false;
                    this.errorStatus = true;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.errorStatus = true;
            });
        }
    },
    mounted() {
        this.getNumbersAndVerify();
    }
}
</script>

<style scoped>
main > div {
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 6.1ch);
  width: 99%;
  flex-direction: column;
}

main > div > span {
  color: lightgray;
}

h1, p{
    text-align: center;
}
</style>