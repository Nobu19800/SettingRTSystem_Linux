/****************************************************************************
** Meta object code from reading C++ file 'FrameComp.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.3.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../FrameComp.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'FrameComp.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.3.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
struct qt_meta_stringdata_FrameComp_t {
    QByteArrayData data[25];
    char stringdata[228];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_FrameComp_t, stringdata) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_FrameComp_t qt_meta_stringdata_FrameComp = {
    {
QT_MOC_LITERAL(0, 0, 9),
QT_MOC_LITERAL(1, 10, 16),
QT_MOC_LITERAL(2, 27, 0),
QT_MOC_LITERAL(3, 28, 11),
QT_MOC_LITERAL(4, 40, 7),
QT_MOC_LITERAL(5, 48, 2),
QT_MOC_LITERAL(6, 51, 7),
QT_MOC_LITERAL(7, 59, 2),
QT_MOC_LITERAL(8, 62, 12),
QT_MOC_LITERAL(9, 75, 12),
QT_MOC_LITERAL(10, 88, 11),
QT_MOC_LITERAL(11, 100, 1),
QT_MOC_LITERAL(12, 102, 12),
QT_MOC_LITERAL(13, 115, 9),
QT_MOC_LITERAL(14, 125, 12),
QT_MOC_LITERAL(15, 138, 3),
QT_MOC_LITERAL(16, 142, 9),
QT_MOC_LITERAL(17, 152, 9),
QT_MOC_LITERAL(18, 162, 10),
QT_MOC_LITERAL(19, 173, 8),
QT_MOC_LITERAL(20, 182, 2),
QT_MOC_LITERAL(21, 185, 8),
QT_MOC_LITERAL(22, 194, 18),
QT_MOC_LITERAL(23, 213, 2),
QT_MOC_LITERAL(24, 216, 11)
    },
    "FrameComp\0UpdateSizeSignal\0\0AddCompSlot\0"
    "ExComp*\0ec\0FEComp*\0fc\0AddCompSlot1\0"
    "AddCompSlot2\0CompLayout*\0c\0AddCompSlot3\0"
    "AddComps2\0InsertComps2\0num\0AddCompsT\0"
    "AddCompsU\0DeleteComp\0QWidget*\0Vl\0"
    "UpdateEC\0std::vector<Rule>&\0rs\0"
    "DeleteFrame"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_FrameComp[] = {

 // content:
       7,       // revision
       0,       // classname
       0,    0, // classinfo
      12,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       1,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   74,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       3,    2,   75,    2, 0x0a /* Public */,
       8,    1,   80,    2, 0x0a /* Public */,
       9,    1,   83,    2, 0x0a /* Public */,
      12,    1,   86,    2, 0x0a /* Public */,
      13,    0,   89,    2, 0x0a /* Public */,
      14,    1,   90,    2, 0x0a /* Public */,
      16,    0,   93,    2, 0x0a /* Public */,
      17,    1,   94,    2, 0x0a /* Public */,
      18,    2,   97,    2, 0x0a /* Public */,
      21,    1,  102,    2, 0x0a /* Public */,
      24,    0,  105,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 4, 0x80000000 | 6,    5,    7,
    QMetaType::Void, 0x80000000 | 6,    7,
    QMetaType::Void, 0x80000000 | 10,   11,
    QMetaType::Void, 0x80000000 | 10,   11,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,   15,
    QMetaType::Void,
    QMetaType::Void, 0x80000000 | 10,   11,
    QMetaType::Void, 0x80000000 | 19, 0x80000000 | 10,   20,   11,
    QMetaType::Void, 0x80000000 | 22,   23,
    QMetaType::Void,

       0        // eod
};

void FrameComp::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        FrameComp *_t = static_cast<FrameComp *>(_o);
        switch (_id) {
        case 0: _t->UpdateSizeSignal(); break;
        case 1: _t->AddCompSlot((*reinterpret_cast< ExComp*(*)>(_a[1])),(*reinterpret_cast< FEComp*(*)>(_a[2]))); break;
        case 2: _t->AddCompSlot1((*reinterpret_cast< FEComp*(*)>(_a[1]))); break;
        case 3: _t->AddCompSlot2((*reinterpret_cast< CompLayout*(*)>(_a[1]))); break;
        case 4: _t->AddCompSlot3((*reinterpret_cast< CompLayout*(*)>(_a[1]))); break;
        case 5: _t->AddComps2(); break;
        case 6: _t->InsertComps2((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 7: _t->AddCompsT(); break;
        case 8: _t->AddCompsU((*reinterpret_cast< CompLayout*(*)>(_a[1]))); break;
        case 9: _t->DeleteComp((*reinterpret_cast< QWidget*(*)>(_a[1])),(*reinterpret_cast< CompLayout*(*)>(_a[2]))); break;
        case 10: _t->UpdateEC((*reinterpret_cast< std::vector<Rule>(*)>(_a[1]))); break;
        case 11: _t->DeleteFrame(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 1:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< ExComp* >(); break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< FEComp* >(); break;
            }
            break;
        case 2:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< FEComp* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        void **func = reinterpret_cast<void **>(_a[1]);
        {
            typedef void (FrameComp::*_t)();
            if (*reinterpret_cast<_t *>(func) == static_cast<_t>(&FrameComp::UpdateSizeSignal)) {
                *result = 0;
            }
        }
    }
}

const QMetaObject FrameComp::staticMetaObject = {
    { &QWidget::staticMetaObject, qt_meta_stringdata_FrameComp.data,
      qt_meta_data_FrameComp,  qt_static_metacall, 0, 0}
};


const QMetaObject *FrameComp::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *FrameComp::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_FrameComp.stringdata))
        return static_cast<void*>(const_cast< FrameComp*>(this));
    return QWidget::qt_metacast(_clname);
}

int FrameComp::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QWidget::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 12)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 12;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 12)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 12;
    }
    return _id;
}

// SIGNAL 0
void FrameComp::UpdateSizeSignal()
{
    QMetaObject::activate(this, &staticMetaObject, 0, 0);
}
QT_END_MOC_NAMESPACE
