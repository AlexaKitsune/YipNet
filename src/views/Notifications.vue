<template>
    <YipNetLayout :user-data="userData" :on-session="onSession">
		<br/>
		
        <main class="mx-auto max-w-[760px] space-y-4">
            <h1 class="text-2xl font-bold">Notifications</h1>

            <NotificationList :limit="50" />
        </main>
    </YipNetLayout>
</template>

<script>
import YipNetLayout from '@/layouts/YipNetLayout.vue'
import NotificationList from '@/components/NotificationList.vue'

export default {
    name: 'Notifications',

    components: {
        YipNetLayout,
        NotificationList
    },

    props: {
        userData: {
            type: Object,
            default: () => ({})
        },
        onSession: {
            type: Boolean,
            default: false
        }
    }
}
</script>