<template>
	<main class="YipNet-MAIN">
	<AlexiconComponent :type="'universalloginregister'" :serviceName="'YipNet'" v-if="!sessionActive" @get-val="() => { sessionActive = true }"/>
	<AlexiconComponent :type="'mainpage'" :highlightBtnColor="'#7701ff'" v-else>
		<AlexiconComponent :type="'searchbar'" :placeholder="'Search'" @get-switch-menu="(val) => menuActive = val"></AlexiconComponent>
		<div class="Alexicon-container">
			<AlexiconComponent :type="'asidemenu'" :active="menuActive" :size="200"></AlexiconComponent>
			<main class="Alexicon-main">

				<PostCreator v-if="postCreatorActive"/>
				<ProfileUser v-if="route  == 'profile'"/>
				<NewsFeed v-if="route == ''"/>
				
			</main>
		</div>
	</AlexiconComponent>
	</main>
</template>

<script>
import AlexiconComponent from './AlexiconComponents/AlexiconComponent.vue';
import PostCreator from './comp/PostCreator.vue';
import NewsFeed from './views/NewsFeed.vue';
import ProfileUser from './views/ProfileUser.vue';

export default {
	components: {
		AlexiconComponent,
		PostCreator,
		NewsFeed,
		ProfileUser,
	},
	name: 'YipNet',
	data(){
		return{
			sessionActive: false,
			menuActive: false,
			route: "",
			postCreatorActive: false,
		}
	},

	methods: {
		autoRoutes(){
			const path = new URL(window.location.href).pathname;
			let pathArray = path.split("/");
			// eslint-disable-next-line
			let x = pathArray.shift();
			this.route = pathArray[0];
		}
	},

	mounted(){
		this.autoRoutes();
		window.addEventListener("popstate", this.autoRoutes);
	},

	created() {
		const originalPushState = history.pushState;
		const originalReplaceState = history.replaceState;
		const triggerAutoRoutes = () => this.autoRoutes();
		history.pushState = function(...args) {
			originalPushState.apply(this, args);
			triggerAutoRoutes();
		};
		history.replaceState = function(...args) {
			originalReplaceState.apply(this, args);
			triggerAutoRoutes();
		};
	},

	beforeUnmount() {
		window.removeEventListener("popstate", this.autoRoutes);
	}
}
</script>

<style>
button{
	color: light-dark(black, white);
	background-color: light-dark(#efedea, #6b6b6b);
	border: none;
	border-radius: 5px;
	padding: 0.5ch 1ch;
	min-width: 10ch;
	cursor: pointer;
}
</style>