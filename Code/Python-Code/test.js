const axios = require("axios");

module.exports = {
  methods: {
    getCancelledLessons() {
      const schulnummer = '7054400';
      const schule = 'bg-dornbirn';
      const url = 'https://klio.webuntis.com/WebUntis/jsonrpc.do?school=' + schulnummer + '&jsonrpc=2.0';
      const benutzer = 'RappLea';
      const schluessel = '46CH7OOCZBFNWGKR';

      const params = {
        id: 1,
        method: 'authenticate',
        params: {
          user: benutzer,
          password: schluessel,
          client: 'CLIENT'
        }
      };

      axios.post(url, params)
        .then(response => {
          const sessionId = response.data.result.sessionId;
          const today = new Date().toISOString().slice(0, 10).replace(/-/g, "");
          const requestOptions = {
            id: 2,
            method: 'getTimetable',
            params: {
              startDate: today,
              endDate: today,
              elementType: 1,
              departmentId: 1 // Assuming department ID 1 for simplicity, you may need to adjust this
            },
            sessionId: sessionId
          };
          return axios.post(url, requestOptions);
        })
        .then(response => {
          const lessons = response.data.result.data;
          let cancelledLessons = 'Ausfallende Stunden heute:\n';
          let foundCancelled = false;
          lessons.forEach(lesson => {
            if (lesson.code === 'cancelled') {
              foundCancelled = true;
              cancelledLessons += lesson.startTime + ' - ' + lesson.endTime + ': ' + lesson.subjects.join(', ') + '\n';
            }
          });
          if (foundCancelled) {
            console.log(cancelledLessons);
          } else {
            console.log('Keine Stunden fallen heute aus.');
          }
        })
        .catch(error => {
          console.error('Fehler beim Abrufen der Daten:', error);
          console.log('Fehler beim Abrufen der Daten. Bitte versuchen Sie es später erneut.');
        });
    },
  },
};
