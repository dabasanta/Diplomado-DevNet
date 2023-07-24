import { defineStore } from "pinia";

const initialState: boolean = false

export const authStore = defineStore("layers", {
  state: () => ({
    selected: initialState,
    isLogged: initialState
  }),
  actions: {
    loggedIn() {
      this.isLogged = true;
    },
    loggedOut(){
      this.isLogged = false;
    }
    /* Push the selected into Layer */
    
   /*  addSelectedLayer(layer: any) {
      const exists = this.selected.find((x: any) => x.id == layer.id);
      if (!exists) {
        this.selected.push(layer);
      }
    }, */
    /* Remove */
   /*  removeSelectedLayer(layer: any) {
      const res = this.selected.filter((x: any) => x.id != layer.id);
      if (res) {
        this.selected = res;
      }
    }, */
  },
});
