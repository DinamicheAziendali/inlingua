console.log('init timetable');
odoo.define('timetable.main', function (require) {
  'use strict';
  console.log('defining timetable');
  var firstStart = true;
  var core = require('web.core');
  var View = require('web.View');
  var Model = require('web.DataModel');


  //var data = require('web.data');
  //var data_manager = require('web.data_manager');
  //var DataExport = require('web.DataExport');
  //var formats = require('web.formats');
  //var common = require('web.list_common');
  //var Model = require('web.DataModel');
  //var Pager = require('web.Pager');
  //var Sidebar = require('web.Sidebar');
  //var utils = require('web.utils');


  var _lt = core._lt;


  const TimetableView = View.extend({
    template:     'Timetable',
    display_name: _lt('Timetable'),
    icon:         'fa-list-ul',
    //require_fields: true,
    defaults:     _.extend({}, View.prototype.defaults, {}),
    scheduler:    null,
    professors:   [],
    courses:      [],


    /**
     * Startup callback
     */
    start: function () {


      //load courses
      this.load_courses()

          //Loading courses
          .then((c) => console.log('courses loaded', c))

          //loading professors
          .then(() => this.load_professors())

          //Loading courses
          .then(c => console.log('professors loaded', c))

          //creating TimeTable
          .then(result => this.init_timetable(result))

          .then(result => this.refresh())
      ;


      this._super();
    },

    init_timetable: function () {
      //require scheduler
      var Scheduler = bryntum.scheduler.Scheduler;
      var Store = bryntum.Store;

      let dToday = luxon.DateTime.local().set({hour: 0, minute: 0, second: 0});

      let aLessons = [];

      this.scheduler = new Scheduler({
        appendTo:   document.getElementById('timetable-container'),
        eventStyle: 'border',
        autoHeight: true,
        rowHeight:  50,

        columns: [
          {text: 'Name', field: 'name', width: 150}
        ],

        startDate:  dToday.toISO(), // '2017-01-01T06:00',
        endDate:    dToday.plus({days: 7}).toISO(),
        viewPreset: 'hourAndDay',

        resources: this.professors.map(p => Object.assign({}, p, {eventColor: 'blue'})),
        //events:   aLessons,
        features:  {
          columnLines:    true,
          eventResize:    true,
          nonWorkingTime: {highlightWeekends: true},
          timeRanges:     {
            showCurrentTimeLine: true,
            showHeaderElements:  true,
            enableResizing:      true
          },
          eventEdit:      {
            // Add extra widgets to the event editor
            extraWidgets: [
              {
                type:         'combo',
                name:         'courseId',
                label:        'Course',
                editable:     false,
                index:        1,
                valueField:   'key',
                displayField: 'label',
                items:        this.courses//['Appointment', 'Internal', 'Meeting']
              }
            ]
          }

        }
      });

      setTimeout(() => document.querySelector('.b-watermark').remove(), 100);

      this.scheduler.eventStore.on({
        add:    event => {
          let d = event.records[0].data;
          let lesson = {
            'name':         d.name,
            'professor_id': d.resourceId,
            'project_id':   d.courseId,
            'start_time':   d.startDate.toUTCString(),
            'end_time':     d.endDate.toUTCString()
          };
          this.create_lesson(lesson);
          // console.log('add', event);
        },
        update: event => {
          let d = event.record.data;
          let lesson = {
            'name':         d.name,
            'professor_id': d.resourceId,
            'project_id':   d.courseId,
            'start_time':   d.startDate.toUTCString(),
            'end_time':     d.endDate.toUTCString()
          };
          this.update_lesson(d.id, lesson);
          console.log('update', event);
        },
        remove: event => {
          let d = event.records[0].data;
          this.delete_lesson(d.id);
        }
      });
    },

    refresh: function () {
      this.load_lessons()
          .then((results) => {
            console.log('found lessons: ', results);
            this.set_data(results);
          });
    },

    load_lessons: function () {
      return new Model('project.task')
          .query(['id', 'name', 'professor_id', 'project_id', 'start_time', 'end_time'])
          .all();
    },

    load_professors: function () {
      return new Model('res.partner', null, [['professor', '=', 'true']])
          .query(['name', 'id'])
          .all()

          //mapping results
          //.then(result => result.map((p) => ({key: p.id, label: p.name})))

          //update instance yUnits
          .then(result => {
            this.professors = result;
            return result;
          });
    },

    set_data: function (data) {
      //const localizeDate = (date) => new Date(luxon.DateTime.fromJSDate(date).local().toString());

      let mappedData = data
          .filter(item => item.start_time && item.end_time && item.professor_id[0] && item.professor_id)
          // { id : 1, resourceId : 1, name : 'Fight crime', startDate : new Date(2018,4,1,9,00), endDate : new Date(2018,4,1,17,00) },
          .map(lesson => ({
                id:         lesson.id,
                startDate:  new Date(`${lesson.start_time} UTC`),
                endDate:    new Date(`${lesson.end_time} UTC`),
                name:       lesson.name,
                resourceId: lesson.professor_id[0]
              })
          );

      this.scheduler.eventStore.data = mappedData;
    },

    create_lesson: function (data) {
      console.log('creating lesson: ', data);
      return new Model('project.task')
          .call('create', [data])
          .fail(() => setTimeout(() => this.refresh(), 100))
          .then(() => setTimeout(() => this.refresh(), 100))
          ;
    },

    update_lesson: function (lessonId, data) {
      console.log('updating lesson: ', data);
      return new Model('project.task')
          .call('write', [[lessonId], data])
          .fail(() => setTimeout(() => this.refresh(), 100))
          .then(() => setTimeout(() => this.refresh(), 100))
          ;
    },

    delete_lesson: function (lessonId) {
      console.log('deleting lesson: ', lessonId);
      return new Model('project.task')
          .call('unlink', [[lessonId]])
          .fail(() => setTimeout(() => this.refresh(), 100))
          .then(() => setTimeout(() => this.refresh(), 100))
          ;
    },

    load_courses: function () {
      console.log('loading courses');
      return new Model('project.project')
          .query(['id', 'name'])
          .all()

          //mapping results
          .then(result => result.map(c => ({key: c.id, label: c.name})))

          .then(result => {
            this.courses = result;
            return result;
          });
    }

  });


  core.view_registry.add('timetable', TimetableView);


  return TimetableView;
});
