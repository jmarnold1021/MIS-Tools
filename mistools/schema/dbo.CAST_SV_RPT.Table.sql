DROP TABLE [dbo].[CAST_SV_RPT]
GO
SET ANSI_NULLS OFF
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CAST_SV_RPT]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[CAST_SV_RPT](
	[CAST_SV_RPT_ID] [int] NOT NULL,
	[CAST_SV_RPT_FLAG] [bit] NOT NULL,
	[CAST_SV_WORK_ID] [varchar](10) NULL,
	[CASTSV_GI01] [varchar](3) NULL,
	[CASTSV_GI03] [varchar](3) NULL,
	[CASTSV_SB00] [varchar](9) NULL,
	[CASTSV_SB02] [varchar](3) NULL,
	[CASTSV_SV01] [varchar](1) NULL,
	[CASTSV_SV03] [varchar](2) NULL,
	[CASTSV_SV04] [varchar](1) NULL,
	[CASTSV_SV05] [varchar](1) NULL,
	[CASTSV_SV06] [varchar](1) NULL,
	[CASTSV_SV08] [varchar](1) NULL,
	[CASTSV_STUDENT_ID] [varchar](9) NULL,
	[CASTSV_KEY_IDX] [varchar](18) NULL,
	[CASTSV_SV09] [varchar](1) NULL,
	[CASTSV_SV10] [varchar](1) NULL,
 CONSTRAINT [PK_SV_RPT_ID] PRIMARY KEY CLUSTERED 
(
	[CAST_SV_RPT_ID] DESC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[DF__CAST_SV_R__CAST___7A57C2F1]') AND type = 'D')
BEGIN
ALTER TABLE [dbo].[CAST_SV_RPT] ADD  DEFAULT ((1)) FOR [CAST_SV_RPT_FLAG]
END
GO
