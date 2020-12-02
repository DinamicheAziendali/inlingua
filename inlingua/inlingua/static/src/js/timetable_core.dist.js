'use strict';

console.log('init timetable');
odoo.define('timetable.main', function (require) {
  'use strict';


  console.log('defining timetable');
  var firstStart = true;

  var core = require('web.core');
  var View = require('web.View');
  var Model = require('web.DataModel'); //var data = require('web.data');
  //var data_manager = require('web.data_manager');
  //var DataExport = require('web.DataExport');
  //var formats = require('web.formats');
  //var common = require('web.list_common');
  //var Model = require('web.DataModel');
  //var Pager = require('web.Pager');
  //var Sidebar = require('web.Sidebar');
  //var utils = require('web.utils');

  var _lt = core._lt;
  //var scheduler ;
  var TimetableView = View.extend({
    template: 'Timetable',
    display_name: _lt('Timetable'),
    icon: 'fa-list-ul',
    //require_fields: true,
    defaults: _.extend({}, View.prototype.defaults, {}),
    scheduler: null,
    workingTime: {
      fromDay: 1,
      toDay: 6,
      fromHour: 8,
      toHour: 22
    },
    professors: [],
    courses: [],

    /**
     * Startup callback
     */
    start: function start() {
      var _this = this;

      //load courses
      this.load_courses() //Loading courses
        .then(function (c) {
          return console.log('courses loaded', c);
        }) //loading professors
        .then(function () {
          return _this.load_professors();
        }) //Loading courses
        .then(function (c) {
          return console.log('professors loaded', c);
        }) //creating TimeTable
        .then(function (result) {
          return _this.init_timetable(result);
        }).then(function (result) {
          return _this.refresh();
        });

      this._super();
    },
    init_timetable: function init_timetable() {
      var _this2 = this;

      //require scheduler
      //var scheduler ; //= bryntum.scheduler.Scheduler;
      var Store = bryntum.Store;
      var WidgetHelper = bryntum.scheduler.WidgetHelper;
      var DateHelper = bryntum.scheduler.DateHelper;
      var Fullscreen = bryntum.scheduler.Fullscreen;



      var dToday = luxon.DateTime.local().set({
        hour: 0,
        minute: 0,
        second: 0
      });

      // Array con le lezioni (Eventi in bryntum)
      var aLessons = [];

      let tools = document.getElementById('timetable-tools') || document.body;
      /*
            if (bryntum.scheduler.Fullscreen.enabled) {
              //if (typeof fullscreenButton == 'undefined') {
              if (!bryntum.scheduler.WidgetHelper.getById('fullscreen-button')) {
                const fullscreenButton = bryntum.scheduler.WidgetHelper.createWidget({
                  type: 'button',
                  id: 'fullscreen-button',
                  icon: 'b-icon b-icon-fullscreen',
                  //tooltip    : this.L('Fullscreen'),
                  toggleable: true,
                  cls: 'b-blue b-raised',
                  keep: true,
                  appendTo: tools,
                  onToggle: ({
                    pressed
                  }) => {
                    if (pressed) {
                      bryntum.scheduler.Fullscreen.request(document.documentElement);
                    } else {
                      bryntum.scheduler.Fullscreen.exit();
                    }
                  }
                });

                bryntum.scheduler.Fullscreen.onFullscreenChange(() => {
                  fullscreenButton.pressed = bryntum.scheduler.Fullscreen.isFullscreen;
                });
              }
            }
      */

      if (Fullscreen.enabled) {

        // Creazione tasto fullscreen
        const fullscreenButton = WidgetHelper.createWidget({
          type: 'button',
          id: 'fullscreen-button',
          //tooltip    : this.L('Fullscreen'),
          toggleable: true,
          cls: 'b-blue b-raised b-icon b-icon-fullscreen ml-10',
          keep: true,

          onToggle: ({ pressed }) => {
            if (pressed) {
              Fullscreen.request(document.documentElement);
            } else {
              Fullscreen.exit();
            }
          }
        });

        // Aggiunta del tasto fullscreen alla toolbar
        WidgetHelper.append(fullscreenButton, { insertFirst: tools || document.body }).this;

        Fullscreen.onFullscreenChange(() => { fullscreenButton.pressed = Fullscreen.isFullscreen; });
      }

      // Selettore data
      WidgetHelper.append([{
        type: 'datefield',
        label: 'Seleziona data',
        width: 220,
        value: new Date(),
        format: 'DD/MM/YYYY',
        editable: false,

        listeners: {
          change: ({ value }) => {
            function getMonday(d) {
              var day = d.getDay(),
                diff = d.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
              return new Date(d.setDate(diff));
            }

            const start = DateHelper.add(getMonday(value), 8, 'hour');
            const end = DateHelper.add(start, 5, 'day');
            return this.scheduler.setTimeSpan(start, end);
          }
        }
      }], {
        insertFirst: tools || document.body
      }).this;


      this.scheduler = new bryntum.scheduler.Scheduler({
        appendTo: document.getElementById('timetable-container'),
        cls: "rounded-div",
        eventStyle: 'colored',
        height: 450,
        rowHeight: 50,
        workingTime: this.workingTime,
        columns: [{
          text: 'Name',
          field: 'name',
          width: 150
        }],
        startDate: dToday.toISO(),
        // '2017-01-01T06:00',
        endDate: dToday.plus({
          days: 7
        }).toISO(),

        viewPreset: {
          displayDateFormat: 'H:mm',
          timeResolution: {
            unit: 'MINUTE',
            increment: 5
          },
          headerConfig: {
            middle: {
              unit: 'HOUR',
              align: 'center',
              dateFormat: 'H'
            },
            top: {
              unit: 'DAY',
              align: 'center',
              dateFormat: 'dddd DD/MM/YYYY'
            }
          },
          columnLinesFor: 0

        },

        //'hourAndDay',
        resources: this.professors.map(function (p) {
          return Object.assign({}, p, {
            eventColor: 'blue'
          });
        }),

        //events:   aLessons,
        features: {
          columnLines: true,
          eventResize: true,
          nonWorkingTime: {
            highlightWeekends: true
          },

          timeRanges: {
            showCurrentTimeLine: true,
            showHeaderElements: true,
            enableResizing: true
          },

          eventEdit: {
            // Add extra widgets to the event editor
            extraItems: [{
              type: 'combo',
              name: 'projectId',
              label: 'Course',
              editable: false,
              index: 1,
              valueField: 'key',
              displayField: 'label',
              store: this.courses, //['Appointment', 'Internal', 'Meeting']
              emptyText: 'seleziona un corso...'
            },
            {
              type: 'textarea',
              name: 'notes',
              label: 'Note',
              valueField: 'notes',
              displayField: 'label'
            },
            {
              type: 'button',
              name: 'recupera',
              text: 'Recupera alla fine',
              icon: 'b-fa-sync-alt',
              onClick: (item) => {
                console.log('click Recupare lezione alla fine', item, arguments, this)
              },
              onAction: ({ source: btn }) => {
                console.log(btn);
              }
            },
            {
              type: 'list',
              name: 'lista_allievi',
              text: 'Allievi',
              items: [{
                nome: "pippo",
                cognome: "Rossi"
              },
              {
                nome: 'pluto',
                cognome: "Verdi"
              },
              {
                nome: 'paperino',
                cognome: "Bianchi"
              }
              ],
              itemTpl: (item) => {
                return '<div><strong>' + item.cognome + '</strong> ' + item.nome + '</div>';
              },
              onClick: (item) => { console.log('click Lista allievi:', item) }
            }
            ]
          }
        }
      });

      this.scheduler.on('cellClick', () => console.log('cellClick'));
      //this.scheduler.on('cellMouseOver', () => console.log('cellMouseover'));

      // setTimeout(function () {
      //   return document.querySelector('.b-watermark').remove();
      // }, 100);

      this.scheduler.eventStore.on({
        // Creazione della lezione
        add: function add(event) {
          console.log(event);
          var d = event.records[0].data;
          var lesson = {
            'name': d.name,
            'professor_id': d.resourceId,
            'project_id': d.projectId,
            'start_time': d.startDate,
            'end_time': d.endDate,
            'notes': d.notes
          };

          _this2.create_lesson(lesson); // console.log('add', event);

        },
        // Aggiornamento lezione
        update: function update(event) {
          var d = event.record.data;
          console.log('date', new Date(d.startDate).toUTCString())



          var lesson = {
            'name': d.name,
            'professor_id': d.resourceId,
            'project_id': d.projectId,
            'start_time': d.startDate,
            'end_time': d.endDate,
            'notes': d.notes
          };

          _this2.update_lesson(d.id, lesson);

          console.log('update', event);
        },
        // Cancellazione lezione
        remove: function remove(event) {
          var d = event.records[0].data;

          _this2.delete_lesson(d.id);
        }
      });
    },
    refresh: function refresh() {
      var _this3 = this;

      this.load_lessons().then(function (results) {
        console.log('found lessons: ', results);

        _this3.set_data(results);
      });
    },
    // Caricamento delle lezioni
    load_lessons: function load_lessons() {
      return new Model('project.task').query(['id', 'name', 'professor_id', 'project_id', 'start_time', 'end_time', 'notes']).all();
    },
    // Caricamento dei professori
    load_professors: function load_professors() {
      var _this4 = this;

      return new Model('res.partner', null, [
        ['professor', '=', 'true']
      ]).query(['name', 'id']).all() //mapping results
        //.then(result => result.map((p) => ({key: p.id, label: p.name})))
        //update instance yUnits
        .then(function (result) {
          _this4.professors = result;
          return result;
        });
    },
    set_data: function set_data(data) {
      //const localizeDate = (date) => new Date(luxon.DateTime.fromJSDate(date).local().toString());
      var mappedData = data.filter(function (item) {
        return item.start_time && item.end_time && item.professor_id[0] && item.professor_id;
      }) // { id : 1, resourceId : 1, name : 'Fight crime', startDate : new Date(2018,4,1,9,00), endDate : new Date(2018,4,1,17,00) },
        .map(function (lesson) {
          if (lesson.name === 'test lezione') {
            console.log('test-lezione', lesson);
          }

          var toLocaleDate = function (timestamp) {
            var date = new Date(timestamp);
            return new Date(date.getTime() - date.getTimezoneOffset() * 60 * 1000);
          }

          return {
            id: lesson.id,
            startDate: toLocaleDate(lesson.start_time),
            endDate: toLocaleDate(lesson.end_time),
            //startDate: new Date(lesson.start_time).toLocaleTimeString(),
            //endDate: new Date(lesson.end_time).to
            name: lesson.name,
            projectId: lesson.project_id[0],
            resourceId: lesson.professor_id[0],
            notes: lesson.notes
          };
        });
      this.scheduler.eventStore.data = mappedData;

      console.log('eventStore.data:', this.scheduler.eventStore.data);
    },
    create_lesson: function create_lesson(data) {
      var _this5 = this;

      console.log('creating lesson: ', data);
      return new Model('project.task').call('create', [data]).fail(function () {
        return setTimeout(function () {
          return _this5.refresh();
        }, 100);
      }).then(function () {
        return setTimeout(function () {
          return _this5.refresh();
        }, 100);
      });
    },
    update_lesson: function update_lesson(lessonId, data) {
      var _this6 = this;

      console.log('updating lesson: ', data);
      return new Model('project.task').call('write', [
        [lessonId], data
      ]).fail(function () {
        return setTimeout(function () {
          return _this6.refresh();
        }, 100);
      }).then(function () {
        return setTimeout(function () {
          return _this6.refresh();
        }, 100);
      });
    },
    delete_lesson: function delete_lesson(lessonId) {
      var _this7 = this;

      console.log('deleting lesson: ', lessonId);
      return new Model('project.task').call('unlink', [
        [lessonId]
      ]).fail(function () {
        return setTimeout(function () {
          return _this7.refresh();
        }, 100);
      }).then(function () {
        return setTimeout(function () {
          return _this7.refresh();
        }, 100);
      });
    },
    load_courses: function load_courses() {
      var _this8 = this;

      console.log('loading courses');
      return new Model('project.project').query(['id', 'name', 'language_id']).all() //mapping results
        .then(result => {
          return result.map(function (c) {
            return {
              key: c.id,
              label: c.name,
              lang: c.language_id
            };
          });
        }).then(function (result) {
          _this8.courses = result;
          return result;
        });
    }
  });

  core.view_registry.add('timetable', TimetableView);

  return TimetableView;
});