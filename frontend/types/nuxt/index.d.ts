import { NuxtAxiosInstance } from "@nuxtjs/axios"
import { accessorType } from "~/store"

declare module "vue/types/vue" {
  interface Vue {
    $accessor: typeof accessorType
    $axios: NuxtAxiosInstance
  }
}

declare module "@nuxt/types" {
  interface NuxtAppOptions {
    $accessor: typeof accessorType
    $axios: NuxtAxiosInstance
  }
}
