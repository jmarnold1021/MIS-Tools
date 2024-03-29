DROP TABLE [dbo].[CAST_CB_RPT]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_CB_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_CB_RPT](
	[CAST_CB_RPT_ID] [int] NOT NULL,
	[CAST_CB_RPT_FLAG] [bit] NOT NULL,
	[CAST_CB_WORK_ID] [varchar](10) NULL,
	[CASTCB_COURSE_ID] [varchar](10) NULL,
	[CASTCB_GI01] [varchar](3) NULL,
	[CASTCB_GI03] [varchar](3) NULL,
	[CASTCB_CB01] [varchar](12) NULL,
	[CASTCB_CB02] [varchar](68) NULL,
	[CASTCB_CB03] [varchar](6) NULL,
	[CASTCB_CB04] [varchar](1) NULL,
	[CASTCB_CB05] [varchar](1) NULL,
	[CASTCB_CB06] [varchar](4) NULL,
	[CASTCB_CB07] [varchar](4) NULL,
	[CASTCB_CB08] [varchar](1) NULL,
	[CASTCB_CB09] [varchar](1) NULL,
	[CASTCB_CB10] [varchar](1) NULL,
	[CASTCB_CB11] [varchar](1) NULL,
	[CASTCB_CB13] [varchar](1) NULL,
	[CASTCB_CB14] [varchar](6) NULL,
	[CASTCB_CB15] [varchar](8) NULL,
	[CASTCB_CB19] [varchar](7) NULL,
	[CASTCB_CB20] [varchar](9) NULL,
	[CASTCB_CB21] [varchar](1) NULL,
	[CASTCB_CB22] [varchar](1) NULL,
	[CASTCB_CB23] [varchar](1) NULL,
	[CASTCB_KEY_IDX] [varchar](18) NULL,
	[CASTCB_CB00] [varchar](12) NULL,
	[CASTCB_CB24] [varchar](1) NULL,
	[CASTCB_CB12] [varchar](1) NULL,
	[CASTCB_CB25] [varchar](1) NULL,
	[CASTCB_CB26] [varchar](1) NULL,
	[CASTCB_CB27] [varchar](1) NULL,
 CONSTRAINT [PK_CB_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_CB_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
