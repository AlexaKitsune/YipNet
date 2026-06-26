<template>
    <MainLayout
        :user-data="userData"
        :on-session="onSession"
    >
        <template #brand>
            <RouterLink to="/">YipNet</RouterLink>
        </template>

        <template #header-actions>
            <UButton to="/" icon="i-lucide-newspaper" variant="ghost" />
            <UButton to="/settings" icon="i-lucide-settings" variant="ghost" />
        </template>

        <template #sidebar="{ closeSidebar }">
            <slot name="sidebar" :close-sidebar="closeSidebar">
                <YipNetSidebar @navigate="closeSidebar" />
            </slot>
        </template>

        <slot />
    </MainLayout>
</template>

<script>
import MainLayout from '@/layouts/MainLayout.vue'
import YipNetSidebar from '@/components/YipNetSidebar.vue'

export default {
    name: 'YipNetLayout',

    components: {
        MainLayout,
        YipNetSidebar
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