/****************************************************************************
** Meta object code from reading C++ file 'SetComp.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.3.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../SetComp.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'SetComp.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.3.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_SetComp_t {
    QByteArrayData data[14];
    char stringdata[116];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_SetComp_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_SetComp_t qt_meta_stringdata_SetComp = {
    {
QT_MOC_LITERAL(0, 0, 7),
QT_MOC_LITERAL(1, 8, 16),
QT_MOC_LITERAL(2, 25, 0),
QT_MOC_LITERAL(3, 26, 1),
QT_MOC_LITERAL(4, 28, 1),
QT_MOC_LITERAL(5, 30, 14),
QT_MOC_LITERAL(6, 45, 4),
QT_MOC_LITERAL(7, 50, 11),
QT_MOC_LITERAL(8, 62, 4),
QT_MOC_LITERAL(9, 67, 4),
QT_MOC_LITERAL(10, 72, 10),
QT_MOC_LITERAL(11, 83, 8),
QT_MOC_LITERAL(12, 92, 11),
QT_MOC_LITERAL(13, 104, 11)
    },
    "SetComp\0UpdateSizeSignal\0\0w\0h\0"
    "UpdateSizeSlot\0save\0const char*\0Name\0"
    "open\0CreateComp\0UpdateEC\0UpdateComps\0"
    "UpdateComp2"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_SetComp[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    2,   54,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       5,    0,   59,    2, 0x0a /* Public */,
       6,    1,   60,    2, 0x0a /* Public */,
       9,    1,   63,    2, 0x0a /* Public */,
      10,    0,   66,    2, 0x0a /* Public */,
      11,    0,   67,    2, 0x0a /* Public */,
      12,    0,   68,    2, 0x0a /* Public */,
      13,    0,   69,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::Int, QMetaType::Int,    3,    4,

 // slots: parameters
    QMetaType::Void,
    QMetaType::Bool, 0x80000000 | 7,    8,
    QMetaType::Bool, 0x80000000 | 7,    8,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,

       0        // eod
};

void SetComp::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        SetComp *_t = static_cast<SetComp *>(_o);
        switch (_id) {
        case 0: _t->UpdateSizeSignal((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 1: _t->UpdateSizeSlot(); break;
        case 2: { bool _r = _t->save((*reinterpret_cast< const char*(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = _r; }  break;
        case 3: { bool _r = _t->open((*reinterpret_cast< const char*(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< bool*>(_a[0]) = _r; }  break;
        case 4: _t->CreateComp(); break;
        case 5: _t->UpdateEC(); break;
        case 6: _t->UpdateComps(); break;
        case 7: _t->UpdateComp2(); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (SetComp::*_t)(int , int );
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&SetComp::UpdateSizeSignal)) {
                *result = 0;
            }
        }
    }
}

const QMetaObject SetComp::staticMetaObject = {
    { &QTabWidget::staticMetaObject, qt_meta_stringdata_SetComp.data,
      qt_meta_data_SetComp,  qt_static_metacall, 0, 0}
};


const QMetaObject *SetComp::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SetComp::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_SetComp.stringdata))
        return static_cast<void*>(const_cast< SetComp*>(this));
    return QTabWidget::qt_metacast(_clname);
}

int SetComp::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QTabWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 8;
    }
    return _id;
}

// SIGNAL 0
void SetComp::UpdateSizeSignal(int _t1, int _t2)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}
QT_END_MOC_NAMESPACE
