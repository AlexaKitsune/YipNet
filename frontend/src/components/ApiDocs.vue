<template>
    <main class="ApiDocs-MAIN">

        <section v-if="lang == 'js'">
            <h3 @click="deploySections(1)">Setting your API key and user ID</h3>
            <div class="sections-api-docs api-doc-1">
                <div v-html="renderCode(jsCodeExample[0])"></div>
            </div>

            <h3 @click="deploySections(2)">Creating post</h3>
            <div class="sections-api-docs api-doc-2">
                <h4>Preparing your data</h4>
                <h5>You can add data to your post in the following way:</h5>
                <div v-html="renderCode(jsCodeExample[1])"></div>

                <h5>You also can add multiple images and videos to your post by adding multiple "media":</h5>
                <div v-html="renderCode(jsCodeExample[2])"></div>
                <h5>It's recommended that you make this recursively.</h5>

                <h4>Submit your post</h4>
                <h5>Request example - Sending data</h5>
                <div v-html="renderCode(jsCodeExample[3])"></div>
            </div>

            <h3 @click="deploySections(3)">Delete post</h3>
            <div class="sections-api-docs api-doc-3">
                <h4>Select the post you want to delete</h4>
                <h5>You need the ID of the post that you will delete:</h5>
                <div v-html="renderCode(jsCodeExample[4])"></div>

                <h4>Deleting</h4>
                <h5>Request example</h5>
                <div v-html="renderCode(jsCodeExample[5])"></div>
            </div>

            <h3 @click="deploySections(4)">List your posts</h3>
            <div class="sections-api-docs api-doc-4">
                <h5><br>All you have to do is make a GET request to the server:</h5>
                <div v-html="renderCode(jsCodeExample[6])"></div>
            </div>

            <h3 @click="deploySections(5)">Retrieve data from an user</h3>
            <div class="sections-api-docs api-doc-5">
                <h4>Select the target user by their ID</h4>
                <h5>This will be the user from which you will extract the information.</h5>
                <h5>Remember that this will only work if the user has allowed the YipNet API to share their information.</h5>
                <div v-html="renderCode(jsCodeExample[7])"></div>

                <h4>Request the data</h4>
                <div v-html="renderCode(jsCodeExample[8])"></div>
            </div>
                
        </section>

        <section v-if="lang == 'py'">
            <h3 @click="deploySections(6)">Import requests module, setting your API key and user ID</h3>
            <div class="sections-api-docs api-doc-6">
                <div v-html="renderCode(pyCodeExample[0])"></div>
                <h5>Make sure you have the requests module installed in your Python environment. You can install it using pip if you don't have it already:</h5>
                <div v-html="renderCode(pyCodeExample[1], 'bash')"></div>
            </div>

            <h3 @click="deploySections(7)">Creating post</h3>
            <div class="sections-api-docs api-doc-7">
                <h4>Preparing your data</h4>
                <h5>You can add data to your post in the following way:</h5>
                <div v-html="renderCode(pyCodeExample[2])"></div>

                <h5>If you want to send images or videos, you need to create a dictionary with the desired data:</h5>
                <div v-html="renderCode(pyCodeExample[3])"></div>

                <h5>Then, create a file dictionary where 'media' is the key and a file is the value:</h5>
                <div v-html="renderCode(pyCodeExample[4])"></div>

                <h4>Submit your post - request example</h4>
                <h5>Send the POST request with the data and API key</h5>
                <div v-html="renderCode(pyCodeExample[5])"></div>
            </div>

            <h3 @click="deploySections(8)">Delete post</h3>
            <div class="sections-api-docs api-doc-8">
                <h4>Select the post you want to delete</h4>
                <h5>You need the ID of the post that you will delete:</h5>
                <div v-html="renderCode(pyCodeExample[6])"></div>

                <h4>Deleting</h4>
                <h5>Request example</h5>
                <div v-html="renderCode(pyCodeExample[7])"></div>
            </div>

            <h3 @click="deploySections(9)">List your posts</h3>
            <div class="sections-api-docs api-doc-9">
                <h5><br>All you have to do is make a GET request to the server:</h5>
                <div v-html="renderCode(pyCodeExample[8])"></div>
            </div>

            <h3 @click="deploySections(10)">Retrieve data from an user</h3>
            <div class="sections-api-docs api-doc-10">
                <h4>Select the target user by their ID</h4>
                <h5>This will be the user from which you will extract the information.</h5>
                <h5>Remember that this will only work if the user has allowed the YipNet API to share their information.</h5>
                <div v-html="renderCode(pyCodeExample[9])"></div>

                <h4>Request the data</h4>
                <div v-html="renderCode(pyCodeExample[10])"></div>
            </div>

        </section>

    </main>
</template>

<script>
import hljs from 'highlight.js';
import 'highlight.js/styles/atom-one-dark.css';
export default {
    name: 'ApiDocs',
    props: {
        lang: String,
        userId: null
    },
    data(){
        return{
jsCodeExample: [
`// Replace "YOUR_API_KEY" with your real key.
const apiKey = "YOUR_API_KEY";\n
const userId = ${this.userId};`,

`const content = {
    "content": "Hello World!"   // String, all the text you want to post.
    "privatePost": false,       // Boolean.
    "nsfwPost" false,           // Boolean.
    "origin": "my App"          // String (optional), the origin that will be displayed on your post.
    "media": fileInput.files[0] // (Optional), assuming 'fileInput' is an input of type 'file'.
}`,

`const content = {
    "content": "Hello World!"
    "privatePost": false,
    "nsfwPost" false,
    "origin": "my App"
    "media": fileInput.files[0],
    "media": fileInput.files[0],
    "media": fileInput.files[0],
    // ...
    "media": fileInput.files[100]
},`,

`formData.append('content', content.content);
formData.append('privatePost', content.privatePost);
formData.append('nsfwPost', content.nsfwPost);
formData.append('origin', content.origin);          // Optional.
formData.append('media', content.media);            // Optional.\n
fetch(\`${this.$ENDPOINT}/api/post/\${userId}\`, {  
        method: 'POST',
        headers: {
            'Authorization': \`Bearer \${apiKey}\`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
    })
    .then(response => {
        console.log(response);
    })
    .catch(error => {
        console.error('Network error:', error);
    });
`,

`const postId = 10;`,

`fetch(\`${this.$ENDPOINT}/api/delete/\${postId}?userId=\${userId}\`, {
        method: 'DELETE',
        headers: {
            'Authorization': \`Bearer \${apiKey}\`,
        }
    })
    .then(response => {
        console.log(response);
    })
    .catch(error => {
        console.error('Network error:', error);
    });`,

`fetch(\`${this.$ENDPOINT}/api/list/\${userId}\`, {
        method: 'GET',
        headers: {
            'Authorization': \`Bearer \${apiKey}\`,
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Posts:', data);
    })
    .catch(error => {
        console.error('Network error:', error);
    });
}`,

`const targetProfile = 1;`,

` fetch(\`${this.$ENDPOINT}/api/get/\${userId}?targetProfile=\${targetProfile}\`, {
        method: 'GET',
         headers: {
            'Authorization': \`Bearer \${apiKey}\`,
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Profile data:', data);
    })
    .catch(error => {
        console.error('Network error:', error);
    });`
],

pyCodeExample: [
`import requests\n
# Replace "YOUR_API_KEY" with your real key.
api_key = "YOUR_API_KEY"\n
user_id = ${this.userId}`,

`pip install requests`,

`content = {
    "content": "Hello World!",  # String, all the text you want to post.
    "privatePost": False,       # Boolean.
    "nsfwPost": False,          # Boolean.
    "origin": "my App"          # String (optional), the origin that will be displayed on your post.
}`,

`data = {
    "content": content["content"],
    "privatePost": content["privatePost"],
    "nsfwPost": content["nsfwPost"],
    "origin": content.get("origin", ""),  # Optional.
}`,

`files = {
    "media": ('filename.jpg', open('route_to_your_file.jpg', 'rb'), 'image/jpeg'),
    # You can add more files here:
    "media": ('filename1.jpg', open('route_to_your_file1.jpg', 'rb'), 'image/jpeg'),
    "media": ('filename2.png', open('route_to_your_file2.png', 'rb'), 'image/png'),
    "media": ('filename3.mp4', open('route_to_your_file3.mp4', 'rb'), 'video/mp4'),
}`,

`response = requests.post(
    f"${this.$ENDPOINT}/api/post/{user_id}",
    data=data,
    files=files,
    headers={'Authorization': f'Bearer {api_key}'}
)\n
print(response)`,

`post_id = 10`,

`response = requests.delete(
    f"${this.$ENDPOINT}/api/delete/{post_id}?userId={user_id}",
    headers={'Authorization': f'Bearer {api_key}'}
)\n
print(response)`,

`try:
    response = requests.get(
        f"${this.$ENDPOINT}/api/list/{user_id}",
        headers={'Authorization': f'Bearer {api_key}'}
    )
    print(response)
except requests.exceptions.RequestException as e:
    print('Network error:', e)`,

`target_profile = 1;`,

`response = requests.delete(
    f"${this.$ENDPOINT}/api/get/{post_id}?targetProfile={target_profile}",
    headers={'Authorization': f'Bearer {api_key}'}
)\n
print(response)`,
],

            responsesCodeExample: [
                `{}`
            ]
        }
    },

    methods:{
        
        renderCode(code_, lang_=false){
            if(lang_ == false)
                lang_ = this.lang;

            let highlightedCode;
            try {
                highlightedCode = hljs.highlight(lang_, code_.replaceAll("$LT;","<").replaceAll("$GT;",">")).value;
            } catch (error) {
                highlightedCode = hljs.highlight("txt", code_.replaceAll("$LT;","<").replaceAll("$GT;",">")).value;
            }
            
            return `<pre style="background-color:rgba(0,0,0,0.3); padding:1ch; border-radius:1ch; overflow:auto;"><code>${highlightedCode}</code></pre>`;
        },

        deploySections(section_){
            document.querySelectorAll(".sections-api-docs").forEach(apiDoc => 
                apiDoc.style.height = "0px"
            );

            if(!section_)
                return;

            document.querySelector(`.api-doc-${section_}`).style.height = "fit-content";
        }
    },
}
</script>

<style scoped>
.ApiDocs-MAIN{
    width: 100%;
}

.ApiDocs-MAIN{
    display: flex;
    flex-direction: column;
    align-items: flex-start !important;
    text-align: left;
}

.ApiDocs-MAIN > section{
    width: calc(100% );
}

.ApiDocs-MAIN > section h3, .ApiDocs-MAIN > section h4, .ApiDocs-MAIN > section h5, p{
    margin-top: 1ch;
}

.ApiDocs-MAIN > section h3{
    margin-bottom: 0;
    margin-top: 3ch;
    background-color: rgba(100, 100, 100, 0.2);
    padding: 0.5ch 1ch;
    border-radius: 1ch;
}

.ApiDocs-MAIN > section h3:hover{
    background-color: rgba(100, 100, 100, 0.4);
    cursor: pointer;
}

.ApiDocs-MAIN > section h5{
    color: lightgray;
}

.ApiDocs-MAIN > section h4{
    margin-top: 3ch;
    margin-bottom: 1ch;
}

.ApiDocs-MAIN > section h5{
    font-weight: 300;
    margin-bottom: 0;
}

.ApiDocs-MAIN > section > div{
    width: 100%;
}

.ApiDocs-MAIN > section *:not(h3){
    margin-left: 2ch;
    max-width: calc(100% - 2ch);
}

.ApiDocs-MAIN > section h5{
    margin-left: 2.5ch;
    max-width: calc(100% - 2.5ch);
}

.sections-api-docs{
    overflow: hidden;
    height: 0px;
    transition: all 0.1s;
}
</style>