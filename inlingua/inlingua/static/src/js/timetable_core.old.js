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
        yUnits:       [],
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
                .then((c) => console.log('professors loaded', c))

                //creating TimeTable
                .then(result => this.init_timetable(result));


            this._super();
        },

        /**
         * Creates timetable structure
         *
         * @param yUnit
         */
        init_timetable: function (yUnit, courses) {
            yUnit = yUnit || this.yUnits;
            courses = courses || this.courses;

            Object.assign(scheduler.config, this.defaults);

            scheduler.locale.labels.timeline_tab = 'Timeline';
            scheduler.locale.labels.section_custom = 'section';
            scheduler.locale.labels.timeline_scale_header = 'Docenti';
            scheduler.config.details_on_create = true;
            scheduler.config.details_on_dblclick = true;
            scheduler.config.first_hour = 9;
            scheduler.config.last_hour = 20;
            scheduler.config.collision_limit = 1;
            scheduler.config.container_autoresize = true;
            scheduler.config.time_step = 15;
            scheduler.config.mark_now = true;
            scheduler.config.xml_date = '%Y-%m-%d %H:%i';

            //FIXME contattare gli amici della timeline per risolvere il bug
            //scheduler.ignore_timeline = date => date.getHours() < 9 || date.getHours() > 20;

            scheduler.blockTime({
                days:  [0, 1, 2, 3, 4, 4, 5, 6],  // marks each weekday
                css:   'noschedule',              // the name of applied CSS class
                zones: [8 * 60, 20 * 60], invert_zones: true //css: 'noschedule'
            });


            scheduler.config.lightbox.sections = [
                {name: 'Nome', height: 30, map_to: 'text', type: 'textarea', focus: true},
                {name: 'Docente', height: 30, type: 'select', options: yUnit, map_to: 'section_id'},
                {name: 'Corso', height: 30, type: 'select', options: courses, map_to: 'project_id'},

                {name: 'Date', height: 30, type: 'time', map_to: 'auto'}
            ];

            var viewConfig = {
                name:            'timeline',
                x_unit:          'minute',
                x_date:          '%H:%i',
                x_step:          30,
                x_size:          15 * 24 * 2,    // X-Axis length specified as the total number of 'x_step's
                x_start:         9 * 2,         // X-Axis offset in 'x_unit's
                x_length:        30 * 2,         // number of 'x_step's that will be scrolled at a time
                y_property:      'section_id',
                render:          'bar',
                event_dy:        'full',
                scrollable:      true,
                column_width:    50,
                autoscroll:      {
                    range_x: 200,
                    range_y: 100,
                    speed_x: 20,
                    speed_y: 10
                },
                second_scale:    {
                    x_unit: 'day',      // the measuring unit of the axis (by default, 'minute')
                    x_date: '%D %d %F'  //the date format of the axis ("mon 01 July")
                },
                scroll_position: new Date()
            };

            scheduler.createTimelineView(Object.assign({}, viewConfig, {y_unit: yUnit}));

            scheduler.attachEvent('onEventChanged', (id, e) => {
                this.update_lesson(parseInt(e.id), {
                    name:         e.text,
                    start_time:   this.offset_time(e.start_date).toISOString(),
                    end_time:     this.offset_time(e.end_date).toISOString(),
                    professor_id: parseInt(e.section_id),
                    project_id:   parseInt(e.project_id)
                });
            });

            scheduler.attachEvent('onEventAdded', (id, e) => {
                this.create_lesson({
                    name:         e.text,
                    start_time:   this.offset_time(e.start_date).toISOString(),
                    end_time:     this.offset_time(e.end_date).toISOString(),
                    project_id:   parseInt(e.project_id),
                    professor_id: parseInt(e.section_id)
                });
            });

            //create TT
            this.scheduler = scheduler;


            setTimeout(() => {
                var schedulerEl = this.$el[0].querySelector('#scheduler_here');
                //schedulerEl.innerHTML = '';
                var thisMorning = new Date();
                thisMorning.setHours(1);

                scheduler.init(schedulerEl, thisMorning, 'timeline');
                this.load_lessons()
                    .then((results) => this.set_data(results));
            }, 10);

        },

        offset_time: function (date) {
            var localeTZ = new Date().getTimezoneOffset();
            var localeOffset = localeTZ * 60 * 1000 * -1;
            var t = new Date();
            t.setTime(date.getTime() + localeOffset);
            return t;
        },

        refresh: function () {
            this.load_lessons()
                .then((results) => this.set_data(results));
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
                .then(result => result.map((p) => ({key: p.id, label: p.name})))

                //update instance yUnits
                .then(result => {
                    this.yUnits = result;
                    return result;
                });
        },

        set_data: function (data) {

            let mappedData = data
                .filter(item => item.start_time && item.end_time && item.professor_id[0] && item.professor_id)
                .map(lesson => ({
                        id:         lesson.id,
                        start_date: lesson.start_time,
                        end_date:   lesson.end_time,
                        text:       lesson.name,
                        section_id: lesson.professor_id[0]
                    })
                );
            scheduler.clearAll();
            scheduler.parse(mappedData, 'json');
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
