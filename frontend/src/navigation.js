import { useRouter } from 'vue-router';

export function goRoute(route) {
  const router = useRouter();
  router.push(route);
}
