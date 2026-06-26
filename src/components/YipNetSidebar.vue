<template>
    <UNavigationMenu
        orientation="vertical"
        :items="items"
        color="neutral"
        :ui="{
            link: 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-[#3a3a3a] hover:text-black dark:hover:text-white',
            linkLeadingIcon: 'text-gray-500 dark:text-gray-400'
        }"
        @click="$emit('navigate')"
    />
</template>

<script>
export default {
    name: 'YipNetSidebar',

    emits: ['navigate'],

    data() {
        return {
            items: [
                {
                    label: this.$t('sidebar.feed'),
                    icon: 'i-lucide-newspaper',
                    to: '/'
                },
                {
                    label: this.$t('sidebar.search'),
                    icon: 'i-lucide-search',
                    to: '/search'
                },
                {
                    label: this.$t('sidebar.chat'),
                    icon: 'i-lucide-message-circle',
                    to: '/chat'
                },
                {
                    label: this.$t('sidebar.notifications'),
                    icon: 'i-lucide-bell',
                    to: '/notifications'
                },
                {
                    label: this.$t('sidebar.settings'),
                    icon: 'i-lucide-settings',
                    to: '/settings'
                }
            ]
        }
    }
}
</script>