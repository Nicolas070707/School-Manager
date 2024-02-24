<template>
  <v-app>
    <v-app-bar app :color="primary" dark class="bar">
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>School-Manager</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn text>{{ currentDate }}</v-btn>
      </v-toolbar-items>
    </v-app-bar>
    <v-footer app :color="primary" dark absolute class="bar">
      <!-- Inhalt der unteren Leiste -->
      <v-toolbar>
        <v-toolbar-title>Widgets</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-menu bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn text v-bind="attrs" v-on="on"> Add Widget </v-btn>
          </template>
          <v-list>
            <v-list-item
              v-for="widget in availableWidgets"
              :key="widget.id"
              @click="addWidget(widget)"
            >
              <v-list-item-title>{{ widget.name }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
    </v-footer>

    <v-navigation-drawer app :color="secondary" dark class="left-bar">
      <v-list dense>
        <v-subheader>User: {{ loggedInUser }}</v-subheader>
        <v-list-item v-for="plugin in connectedPlugins" :key="plugin.id">
          <v-list-item-icon>
            <v-icon>{{ plugin.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ plugin.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <!-- Main content of the app -->
      <v-container fluid>
        <!-- Your app's content here -->
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      currentDate: "",
      loggedInUser: "John Doe", // Beispielbenutzer, durch den tatsächlich angemeldeten Benutzer ersetzen
      connectedPlugins: [
        { id: 1, name: "Plugin 1", icon: "mdi-plugin-1" },
        { id: 2, name: "Plugin 2", icon: "mdi-plugin-2" },
        // Weitere Plugins nach Bedarf hinzufügen
      ],
      widgets: [
        { id: 1, name: "Weather" },
        { id: 2, name: "Notes" },
        // Weitere Widgets nach Bedarf hinzufügen
      ],
      primary: "#D9D9D9", // Aktualisierter Farbcode im HEX-Format
      secondary: "#292727",
    };
  },
  methods: {
    addWidget(widget) {
      // Widget zum Array hinzufügen und initial auf (0, 0) positionieren
      this.widgets.push({ ...widget, x: 0, y: 0 });
    }
  },
  methods: {
    setCurrentDate() {
      const now = new Date();
      const options = { year: "numeric", month: "long", day: "numeric" };
      this.currentDate = now.toLocaleDateString("de-DE", options);
    },
  },
};
</script>

<style scoped>
.bar {
  height: 80px; /* Höhe der oberen Leiste */
}



.left-bar {
  width: 80px; /* Breite der linken Leiste */
  height: auto;
}


</style>
